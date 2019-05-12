package main

import (
	"log"
	"os"
	"strings"
	format "github.com/labstack/gommon/color"
	"bufio"
	"fmt"
	"encoding/csv"
	"io"
	"io/ioutil"
	"strconv"
	"time"
)

var (
	print     = format.Println
	costs = make(map[string]string)
)

func main() {

	// main menu
    mainMenu()
	
}

func mainMenu() {
	for {
		print(format.Underline("\nWelcome to the CallRoutes API!"))
		print(format.Cyan(fmt.Sprintf("\n%d route costs currently loaded in memory.\n", len(costs))))
		print(format.Green("1.) Load File into Memory"))
		print(format.Green("2.) Lookup cost for a number"))
		print(format.Green("3.) Lookup costs for all numbers in a file"))
		print(format.Green("4.) Write results for all numbers in a file to a file"))
		print(format.Red("5.) Exit"), "\n")
		print("Please make a selection:")
		choice := getInput()
		switch choice {
		case "1":
			loadFile()
		case "2":
			getCost()
		case "3":
			getCosts(false)
		case "4":
			getCosts(true)
		case "5":
			return
		default:
			print(format.Magenta("\nInvalid input!"))
		}
	}
}

// Wait for input
func getInput() string {
	buf := bufio.NewReader(os.Stdin)
	fmt.Print("> ")
	sentence, _ := buf.ReadString('\n')
	return strings.Replace(sentence, "\n", "", -1)
}

func loadFile() {

	// get list of files in dir
	allFiles, _ := ioutil.ReadDir("../data")

	// print message
	print(format.Underline("\nLoad a file:"), "\n")

	// create filtered slice of files
	files := []os.FileInfo{}
	for _, file := range allFiles {
		if strings.Contains(file.Name(), "route") {
			files = append(files, file)
		}
	}
	for i := 1; i <= len(files); i++ {
		print(i, ".) ", files[i-1].Name())
	}
	print(format.Red("q.) Main Menu"), "\n")
	print("Please make a selection:")
	choice := getInput()
	index, err := strconv.Atoi(choice)
	if err != nil {
		return
	}

	// start timer
	start := time.Now()

	// open file and defer close
	file, err := os.Open("../data/"+files[index-1].Name())
	if err != nil {
		log.Fatalf("Unable to open file %s: %s\n", files[index-1].Name(), err.Error())
	}
	defer file.Close()

	// create csv reader for file
	reader := csv.NewReader(file)

	// loop through all file lines
	for {

		// read row (file line)
		row, err := reader.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			log.Fatalf("Error while parsing file %s\n", err.Error())
		}
		// insert row into map if not in map or less 
		// than value already in map
		if v, ok := costs[row[0]]; (ok && v > row[1]) || !ok {
			costs[row[0]] = row[1]
		}
		
	}

	print(format.Yellow(fmt.Sprintf("\nCompleted in %v.", time.Since(start))))
}

func getCost() {

	// print message and wait for input
	print("\n", format.Cyan("Enter a number with the prefix:"))
	input := getInput()

	// find longest matching prefix
	result := "0"
	for i := len(input); i >= 0; i-- {
		if v, ok := costs[input[:i]]; ok {
			result = v
		}
	}

	// print result
	print("\n", format.Magenta("Cost:"),format.Bold(format.Green(fmt.Sprintf("%s : %s",input, result))))
	
}

func getCosts(persist bool) {
	// get list of files in dir
	allFiles, _ := ioutil.ReadDir("../data")

	// print message
	print(format.Underline("\nLoad a file:"), "\n")

	// create filtered slice of files
	files := []os.FileInfo{}
	for _, file := range allFiles {
		if strings.Contains(file.Name(), "phone") {
			files = append(files, file)
		}
	}
	for i := 1; i <= len(files); i++ {
		print(i, ".) ", files[i-1].Name())
	}
	print(format.Red("q.) Main Menu"), "\n")
	print("Please make a selection:")
	choice := getInput()
	index, err := strconv.Atoi(choice)
	if err != nil {
		return
	}

	// start timer
	start := time.Now()

	// open file and defer close
	file, err := os.Open("../data/"+files[index-1].Name())
	if err != nil {
		log.Fatalf("Unable to open file %s: %s\n", files[index-1].Name(), err.Error())
	}
	defer file.Close()

	// create csv reader for file
	reader := csv.NewReader(file)

	var resultFile *os.File
	if persist {
		err = os.Mkdir("results", os.ModePerm)
		resultFile, err = os.Create("./results/"+ files[index-1].Name())
		if err != nil {
			print(err)
		}
	}
	defer resultFile.Close()

	// loop through all file lines
	for {

		// read row (file line)
		row, err := reader.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			log.Fatalf("Error while parsing file %s\n", err.Error())
		}

		// find longest matching prefix
		result := "0"
		for i := len(row[0]); i >= 0; i-- {
			if v, ok := costs[row[0][:i]]; ok {
				result = v
			}
		}

		// if persist, append to result file
		if persist {
			_, err := resultFile.WriteString(fmt.Sprintf("%s,%s\n",row[0], result))
			if err != nil {
				print(err)
			}
		} else {
			// otherwise, print result
			print("\n", format.Magenta("Cost:"),format.Bold(format.Green(fmt.Sprintf("%s : %s",row[0], result))))
		}	
		
	}

	// if persist, sync file to disk
	if persist {
		resultFile.Sync()
		print(format.Magenta(fmt.Sprintf("\nResult file /results/%s created!", files[index-1].Name())))
	}

	print(format.Yellow(fmt.Sprintf("\nCompleted in %v.", time.Since(start))))
}