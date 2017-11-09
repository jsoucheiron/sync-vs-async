package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"path"
	"strconv"
	"strings"
	"time"
)

var host, port string

func main() {
	flag.StringVar(&host, "host", "", "Host to serve")
	flag.StringVar(&port, "port", "8080", "Port to listen into")
	flag.Parse()

	http.HandleFunc("/", mainHandler)

	log.Printf("Server listening in %s", host+":"+port)
	err := http.ListenAndServe(host+":"+port, nil)
	if err != nil {
		log.Fatalf(err.Error())
	}
}

// mainHandler routes requests to the appropriate handler. if none
// available, returns 404
func mainHandler(w http.ResponseWriter, r *http.Request) {
	defer startTimer(fmt.Sprintf("mainhandler request with path %s", r.URL.Path))()
	var head string
	head, r.URL.Path = ShiftPath(r.URL.Path) // overwrite request path

	switch head {
	case "io":
		ioHandler(w, r)
	case "cpu":
		cpuHandler(w, r)
	default:
		http.Error(w, "Not Found", http.StatusNotFound)
		log.Printf("Path not found for %s\n", r.URL.Path)
	}
}

// ioHandler receives requests to path of the form '/io/100ms' and
// redirects the request to nginx host
func ioHandler(w http.ResponseWriter, r *http.Request) {
	// Remove leading '/'
	delay := r.URL.Path[1:]
	// Time and log handler execution
	defer startTimer(fmt.Sprintf("iohandler request with delay %s", delay))()

	// Create request for nginx host
	req, err := http.NewRequest("GET", "http://nginx/"+delay, nil)
	if err != nil {
		// Couldn't create the Request
		log.Println(err)
		return
	}

	client := &http.Client{} // Client to perform the request
	resp, err := client.Do(req)
	if err != nil {
		// Request failed
		log.Println(err)
		return
	}
	// Return request's response to caller
	if err := resp.Write(w); err != nil {
		// Writing response failed
		log.Println(err)
		return
	}

	// Everything peachy!
	fmt.Fprintf(w, "Request finished!")
}

// cpuHandler receives requests to path of the form '/cpu/8' and loops
// that many times before returning
func cpuHandler(w http.ResponseWriter, r *http.Request) {
	// Remove leading '/'
	param := r.URL.Path[1:]
	// Time and log handler execution
	defer startTimer(fmt.Sprintf("cpuhandler with iterations %s", param))()

	// Cast parameter to integer
	iterations, err := strconv.Atoi(param[1:])
	if err != nil {
		// Cast failed
		http.Error(w, "Bad Request", http.StatusBadRequest)
		log.Printf("Failed to parse '%s' as integer\n", param[1:])
		return
	}

	// Loop as many times as requested
	for iterations > 0 {
		iterations--
	}
	// Everything peachy!
	fmt.Fprintf(w, "Request finished!")
}

// ShiftPath splits off the first component of p, which will be cleaned of
// relative components before processing. head will never contain a slash and
// tail will always be a rooted path without trailing slash.
func ShiftPath(p string) (head, tail string) {
	p = path.Clean("/" + p)
	i := strings.Index(p[1:], "/") + 1
	if i <= 0 {
		return p[1:], "/"
	}
	return p[1:i], p[i:]
}

// startTimer annotates in the log the beginning of a timer with
// message 'name' and returns a function to stop the timer with a
// similar message and the duration
func startTimer(name string) func() {
	t := time.Now()
	log.Println(name, "started")
	return func() {
		d := time.Now().Sub(t)
		log.Println(name, "took", d)
	}
}
