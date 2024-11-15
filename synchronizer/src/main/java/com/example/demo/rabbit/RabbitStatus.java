package com.example.demo.rabbit;

public enum RabbitStatus {
    
    SUCCESS(200, "Successfully connected to RabbitMQ"),
    ERROR(500, "Error: Is RabbitMQ running at");

    private final int code;
    private final String message;

    RabbitStatus(int code, String message) {
        this.code = code;
        this.message = message;
    }

    public String getErrorMessage(String host, String port) {
        return message + " " + host + ":" + port + " ?";
    }

    public String getMessage() {
        return message;
    }

    public int getCode() {
        return code;
    }
}
