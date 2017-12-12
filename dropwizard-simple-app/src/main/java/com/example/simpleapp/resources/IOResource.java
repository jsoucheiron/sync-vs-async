package com.example.simpleapp.resources;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.util.EntityUtils;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import java.io.IOException;

@Path("/")
public class IOResource {
    private final HttpClient client;

    public IOResource(HttpClient client) {
        this.client = client;
    }

    @GET
    @Path("/io")
    @Produces(MediaType.TEXT_PLAIN)
    public String io(@QueryParam("delay") String delay) throws IOException {
        String url = "http://nginx/" + delay;
        HttpGet request = new HttpGet(url);
        HttpResponse response = client.execute(request);
        HttpEntity entity = response.getEntity();
        String s = EntityUtils.toString(entity);
        return "Request finished!";
    }
}
