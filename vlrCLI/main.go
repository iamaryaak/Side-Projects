// Author: Arya
// Built with: https://tutorialedge.net/golang/consuming-restful-api-with-go/
// Query to this API - https://vlrggapi.vercel.app

/**
 * Querying for VALORANT news
 */
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

// A Response struct to map the Entire Response
type Response struct {
	Data jsonData `json:"data"`
}

// A Pokemon Struct to map every pokemon to.
type jsonData struct {
	Status   int            `json:"status"`
	Segments []newsSegments `json:"segments"`
}

// A struct to map our Pokemon's Species which includes it's name
type newsSegments struct {
	Title   string `json:"title"`
	UrlPath string `json:"url_path"`
}

func main() {
	response, err := http.Get("https://vlrggapi.vercel.app/news/")
	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}

	responseData, err := ioutil.ReadAll(response.Body)
	//fmt.Println(responseData)
	if err != nil {
		fmt.Print(err.Error())
		log.Fatal(err)
	}

	// check if we're getting data
	//fmt.Println("-- First Article --")
	var responseObject Response
	json.Unmarshal(responseData, &responseObject)

	//fmt.Println(responseObject.Data.Segments[0].Title)

	// get top 3 articles from VLR
	for i := 0; i < 3; i++ {
		fmt.Println(responseObject.Data.Segments[i].Title)
		fmt.Println("URL Path: https://vlr.gg" + responseObject.Data.Segments[i].UrlPath)
	}

}
