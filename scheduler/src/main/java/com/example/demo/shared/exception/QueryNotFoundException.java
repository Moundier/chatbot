package com.example.demo.shared.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(code = HttpStatus.NOT_FOUND, reason = "Query not Found")
public class QueryNotFoundException extends RuntimeException {
  
}
