package com.example.simpleapp;

import com.example.simpleapp.resources.CPUResource;
import com.example.simpleapp.resources.IOResource;
import io.dropwizard.Application;
import io.dropwizard.client.HttpClientBuilder;
import io.dropwizard.configuration.EnvironmentVariableSubstitutor;
import io.dropwizard.configuration.SubstitutingSourceProvider;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;
import org.apache.http.client.HttpClient;


public class SimpleApp extends Application<SimpleAppConfiguration> {
    public static void main(String[] args) throws Exception {
        new SimpleApp().run(args);
    }

    @Override
    public String getName() {
        return "simple-dropwizard-app";
    }

    @Override
    public void initialize(Bootstrap<SimpleAppConfiguration> bootstrap) {
        // Enable variable substitution with environment variables
        bootstrap.setConfigurationSourceProvider(
                new SubstitutingSourceProvider(
                        bootstrap.getConfigurationSourceProvider(),
                        new EnvironmentVariableSubstitutor(false)
                )
        );
    }

    @Override
    public void run(SimpleAppConfiguration configuration, Environment environment) {
        final HttpClient httpClient = new HttpClientBuilder(environment)
                .using(configuration.getHttpClientConfiguration())
                .build(getName());
        environment.jersey().register(new IOResource(httpClient));
        environment.jersey().register(new CPUResource());
    }
}
