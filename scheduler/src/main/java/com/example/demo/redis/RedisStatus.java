package com.example.demo.redis;

public enum RedisStatus {
    
    SUCCESS(200, "Successfully connected to Redis"),
    ERROR(500, "Error: Is Redis running at");

    private final int code;
    private final String message;

    RedisStatus(int code, String message) {
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