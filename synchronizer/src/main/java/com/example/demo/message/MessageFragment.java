package com.example.demo.message;

import java.util.Map;

import lombok.Builder;
import lombok.Data;
import lombok.ToString;

@Data
@ToString
@Builder
public class MessageFragment {
    
    private String id;
    private String content;
    private String from;
    private String to;
    private Number timestamp; 
    private String phoneNumber;
    private PossibleNames possibleNames;

    @Data
    private static class PossibleNames {
        private String name;
        private String shortName;
        private String pushname;
    }
}
