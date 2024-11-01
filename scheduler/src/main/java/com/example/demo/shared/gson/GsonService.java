package com.example.demo.shared.gson;

import java.lang.reflect.Type;

import org.springframework.stereotype.Service;

import com.google.gson.Gson;

@Service
public class GsonService {

    private final Gson gson;

    public GsonService() {
      this.gson = new Gson(); 
    }

    public <T> String serialize(T object) {
      return gson.toJson(object);
    }

    public <T> T deserialize(String json, Class<T> clazz) {
      return gson.fromJson(json, clazz);
    }

    public <T> T deserialize(String json, Type type) {
      return gson.fromJson(json, type);
    }
}
