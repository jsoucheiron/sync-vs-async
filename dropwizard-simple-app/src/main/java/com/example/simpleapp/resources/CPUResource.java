package com.example.simpleapp.resources;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;

@Path("/")
public class CPUResource {
    @GET
    @Path("/cpu")
    @Produces(MediaType.TEXT_PLAIN)
    public String cpu(@QueryParam("iterations") String iterations) {
        int i = Integer.parseInt(iterations);
        while(i >= 0)
        {
            i -= 1;
        }
        return "Request finished!";
    }
}
