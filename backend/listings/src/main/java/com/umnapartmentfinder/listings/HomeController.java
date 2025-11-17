package com.umnapartmentfinder.listings;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class HomeController {
    
    // "/" represents the root of website
    @RequestMapping("/")
    public String index() {
        return "index.html";
    }
    
}
