// ==================================================================================
// File: main.go
//
// Desc: Call Routing project solution file in Go. This is the main solution as a 
//       longer startup time is an acceptable tradeoff for near constant time 
//       lookups. In a realistic scenario, the server would stay running anyways so 
//       this tradoff would be negligible.
//
// Copyright © 2019 Edwin Cloud. All rights reserved.
// ==================================================================================
package main

// ----------------------------------------------------------------------------------
// Imports
// ----------------------------------------------------------------------------------
import (
	"os"
	"strings"
	format "github.com/labstack/gommon/color"
	"bufio"
	"fmt"
	"encoding/csv"
	"io"
	"io/ioutil"
	"strconv"
	"errors"
	"time"
)

// ----------------------------------------------------------------------------------
// Global Variables
// ----------------------------------------------------------------------------------
var (
	print     = format.Println
	costs = make(map[string]string)
)

// ----------------------------------------------------------------------------------
// Global Functions
// ----------------------------------------------------------------------------------

// main is the main entry point of the program.
func main() {
    for {
		print(format.Underline("\nWelcome to the CallRoutes API!"))
		print(format.Cyan(fmt.Sprintf("\n%d route costs currently loaded in memory.\n", len(costs))))
		print(format.Green("1.) Load File into Memory"))
		print(format.Green("2.) Lookup cost for a number"))
		print(format.Green("3.) Lookup costs for all numbers in a file"))
		print(format.Green("4.) Write resulting costs for all numbers in a file to a file"))
		print(format.Red("5.) Exit"), "\n")
		print("Please make a selection:")
		choice := getInput()
		switch choice {
		case "1":
			loadRouteCosts()
		case "2":
			print("\n", format.Cyan("Enter a number with the prefix:"))
			prefix := getInput()
			result := getCost(prefix)
			print("\n", format.Magenta("Cost:"),format.Bold(format.Green(fmt.Sprintf("%s : %s", prefix, result))))
		case "3":
			getAllCosts(false) // do not persist to disk
		case "4":
			getAllCosts(true) // persist to disk
		case "5":
			return
		default:
			print(format.Magenta("\nInvalid input!"))
		}
	}
}

// getInput waits for input from stdin and returns the input as a
// string once the `Enter` key is pressed stripped of new lines.
func getInput() string {
	buf := bufio.NewReader(os.Stdin)
	fmt.Print("> ")
	sentence, _ := buf.ReadString('\n')
	return strings.Replace(sentence, "\n", "", -1)
}

// listFiles lists all files in the ../data directory that match
// a filter as choices to stdout. The selected file name and
// an error or nil is returned.
func listFiles(filter string) (string, error) {

	// get list of files in dir
	allFiles, err := ioutil.ReadDir("../data")
	if err != nil {
		return "", err
	}

	// print message
	print(format.Underline("\nLoad a file:"), "\n")

	// create filtered slice of files
	files := []os.FileInfo{}
	for _, file := range allFiles {
		if strings.Contains(file.Name(), filter) {
			files = append(files, file)
		}
	}

	// print choices to stdout
	for i := 1; i <= len(files); i++ {
		print(i, ".) ", files[i-1].Name())
	}
	print(format.Red("q.) Main Menu"), "\n")
	print("Please make a selection:")

	// wait for input
	choice := getInput()

	// ensure choice was valid or return error
	index, err := strconv.Atoi(choice)
	if err != nil {
		return "", errors.New("")
	} else if index < 0 || index >= len(files) {
		return "", errors.New("invalid option: index out of range")
	}

	// return file name and nil error
	return files[index-1].Name(), nil
}

// loadRouteCosts loads route costs from a selected route-costs
// data file into the global variable costs type map[string]string.
func loadRouteCosts() {

	// list available route-costs files, wait for a selection,
	// ensure selection is valid, and get file name
	fileName, err := listFiles("route")
	if err != nil {
		print("\n", format.Red(err.Error()))
		return
	}

	// start timer
	start := time.Now()

	// open selected route-costs file and defer it to close 
	// when this function returns
	file, err := os.Open("../data/"+fileName)
	if err != nil {
		print("\n", format.Red(err.Error()))
		return
	}
	defer file.Close()

	// create csv reader for file
	reader := csv.NewReader(file)

	// loop through all file lines
	for {

		// read row (file line)
		row, err := reader.Read()
		if err == io.EOF {
			// once we hit the end-of-file, break from loop
			break
		} else if err != nil {
			print("\n", format.Red(err.Error()))
			return
		}

		// if current row is in costs map and its cost is less than 
		// current cost in costs map or if current row is not in 
		// costs map
		if v, ok := costs[row[0]]; (ok && v > row[1]) || !ok {
			// insert or update current row into costs map
			costs[row[0]] = row[1]
		}
	}

	// print runtime for function
	print(format.Yellow(fmt.Sprintf("\nCompleted in %v.", time.Since(start))))
}

// getCost gets the cost for a given prefix by searching the costs map
// for the longest matching prefix.
func getCost(prefix string) string {

	// set result equal to 0 by default
	result := "0"

	// find longest matching prefix
	for i := len(prefix); i >= 0; i-- {
		if v, ok := costs[prefix[:i]]; ok {
			result = v
		}
	}

	// return result
	return result
}

// getAllCosts prints all costs for a selected phone-numbers file to stdout
// if persist is false, otherwise the costs are written to a file in /results
func getAllCosts(persist bool) {

	// list available phone-numbers files, wait for a selection,
	// ensure selection is valid, and get file name
	fileName, err := listFiles("phone")
	if err != nil {
		print("\n", format.Red(err.Error()))
		return
	}

	// start timer
	start := time.Now()

	// open selected phone-numbers file and defer it to close 
	// when this function returns
	file, err := os.Open("../data/"+fileName)
	if err != nil {
		print("\n", format.Red(err.Error()))
		return
	}
	defer file.Close()

	// create csv reader for file
	reader := csv.NewReader(file)

	// create resultFile variable and create the file if 
	// persist argument is true, defer file to close when
	// this function returns
	var resultFile *os.File
	if persist {
		err = os.Mkdir("results", os.ModePerm)
		resultFile, err = os.Create("./results/"+ fileName)
		if err != nil {
			print("\n", format.Red(err.Error()))
			return
		}
	}
	defer resultFile.Close()

	// loop through all file lines
	for {

		// read row (file line)
		row, err := reader.Read()
		if err == io.EOF {
			// once we hit the end-of-file, break from loop
			break
		} else if err != nil {
			print("\n", format.Red(err.Error()))
			return
		}

		// get cost for current row's prefix
		cost := getCost(row[0])

		// if persist argument is true, append to result file
		if persist {
			_, err := resultFile.WriteString(fmt.Sprintf("%s,%s\n",row[0], cost))
			if err != nil {
				print("\n", format.Red(err.Error()))
				return
			}
		// otherwise, print the result to stdout
		} else {
			print("\n", format.Magenta("Cost:"),format.Bold(format.Green(fmt.Sprintf("%s : %s",row[0], cost))))
		}	
		
	}

	// if persist argument is true, sync result file to disk and
	// print success message
	if persist {
		resultFile.Sync()
		print(format.Magenta(fmt.Sprintf("\nResult file /results/%s created!", fileName)))
	}

	// print runtime for function
	print(format.Yellow(fmt.Sprintf("\nCompleted in %v.", time.Since(start))))
}