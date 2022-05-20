/*********************************
* Class: MAGSHIMIM C2			 *
* Week:                			 *
* Name:                          *
* Credits:                       *
**********************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "dirent.h"

#define STRING_LENGTH 50

char chooseScanning();
void ilerateFolder(DIR* d, struct dirent* dir, char* folderName, FILE* sign, FILE* logFile, bool normal);
void normalScan(FILE* file, FILE* sign, FILE* logFile);
void quickScan(FILE* file, FILE* sign, FILE* logFile);
bool checkFiles(FILE* file, FILE* sign);
void writeIntoFile(FILE* log, char* text);
void sortFileNames(char** names, int length);

int main(int argc, char** argv)
{
	DIR* d = 0;
	struct dirent* dir = 0;
	FILE* signiture = NULL;
	FILE* logFile = NULL;
	char userChoice = 0;
	if(argc != 3)
	{
		printf("Invalid Input\nRUN THIS:\nprog {The address of the folder} {The address of the virus signiture file}\n");
		return 1;
	}

	d = opendir(argv[1]);
	if (d == NULL)
	{
		printf("Error openning folder\n");
		return 1;
	}

	signiture = fopen(argv[2], "rb");
	if (signiture == NULL)
	{
		printf("Error openning file\n");
		return 1;
	}

	logFile = fopen("AntiVirusLog.txt", "w");
	if (logFile == NULL)
	{
		printf("Error openning file\n");
		return 1;
	}

	printf("Welcome to the virus scanner!\n\n");
	printf("Folder to scan: %s\n", argv[1]);
	printf("Virus signiture: %s\n", argv[2]);
	writeIntoFile(logFile, "Anti-virus began! Welcome!\n\n");
	fclose(logFile);

	logFile = fopen("AntiVirusLog.txt", "a");
	if (logFile == NULL)
	{
		printf("Error openning file\n");
		return 1;
	}

	writeIntoFile(logFile, "Folder to scan:\n");
	writeIntoFile(logFile, argv[1]);
	writeIntoFile(logFile, "\nVirus signature:\n");
	writeIntoFile(logFile, argv[2]);
	writeIntoFile(logFile, "\n\nScanning option:\n");

	userChoice = chooseScanning();
	userChoice == '0' ? writeIntoFile(logFile, "Normal scan\n\n") : writeIntoFile(logFile, "Quick scan\n\n");
	writeIntoFile(logFile, "Results:\n");

	ilerateFolder(d, dir, argv[1], signiture, logFile, userChoice);

	closedir(d);
	fclose(signiture);
	fclose(logFile);

	getchar();
	return 0;
}

void writeIntoFile(FILE* log, char* text)
{
	int index = 0;
	char ch = text[index];
	while (ch != NULL)
	{
		fputc(ch, log);
		index++;
		ch = text[index];
	}
}

char chooseScanning()
{
	char option = ' ';
	printf("Enter 0 for a normal scan and any other key for a quick scan: ");
	scanf("%c", &option);
	getchar();
	return option;
}

void ilerateFolder(DIR* d, struct dirent* dir, char* folderName, FILE* sign, FILE* logFile, bool normal)
{
	char* fileName = NULL;
	FILE* checkedFile = NULL;
	int i = 0, length = 0, j = 0;
	char** namesArray = (char**)malloc(0);
	char* fileNameString = NULL;
	int namesArrayLength = 0;
	while ((dir = readdir(d)) != NULL)
	{
		if (!(strcmp(dir->d_name, ".") == 0 || strcmp(dir->d_name, "..") == 0))
		{
			namesArray = (char**)realloc(namesArray, (namesArrayLength + 1) * sizeof(char*));
			namesArray[namesArrayLength] = dir->d_name;
			printf("%s\n", namesArray[namesArrayLength]);
			namesArrayLength++;
		}
	}
	//printf("%ssomething\n", namesArray[j]);
	//while (j < namesArrayLength)
	for(j = 0; j < namesArrayLength; j++)
	{
		fileNameString = namesArray[j];
		length = strlen(folderName) + strlen(fileNameString) + 2;
		fileName = (char*)malloc(length);
		if (fileName == NULL)
		{
			printf("Unsuccessful malloc\n");
			return NULL;
		}
		for (i = 0; i < length; i++)
		{
			fileName[i] = '\0';
		}
		strcpy(fileName, folderName);
		strncat(fileName, "/", 1);
		strncat(fileName, namesArray[j], strlen(namesArray[j]));
		checkedFile = fopen(fileName, "rb");
		if (checkedFile == NULL)
		{
			printf("Error openning file\n");
			free(fileName);
			return NULL;
		}
		printf("%s/%s - ", folderName, namesArray[j]);
		writeIntoFile(logFile, folderName);
		writeIntoFile(logFile, namesArray[j]);
		writeIntoFile(logFile, " - ");
		normal ? normalScan(checkedFile, sign, logFile) : quickScan(checkedFile, sign, logFile);
		fclose(checkedFile);
		free(fileName);
		free(namesArray);
	}
}

void normalScan(FILE* file, FILE* sign, FILE* logFile)
{
	char firstInSign = NULL, fileChar = ' ';
	bool infected = false;
	fread(&firstInSign, sizeof(char), 1, sign);
	fseek(sign, 0, SEEK_SET);
	while(!infected && !feof(file))
	{
		fread(&fileChar, sizeof(char), 1, file);
		if (fileChar == firstInSign)
		{
			if(checkFiles(file, sign))
			{
				infected = true;
			}
		}
	}
	infected ? printf("Infected!\n") : printf("Clean\n");
	infected ? writeIntoFile(logFile, "Infected!\n") : writeIntoFile(logFile, "Clean\n");

}

void quickScan(FILE* file, FILE* sign, FILE* logFile)
{
	char signChar = ' ', fileChar = ' ';
	bool infected = false;
	fseek(file, 0, SEEK_END);
	int length = ftell(file);
	fseek(file, 0, SEEK_SET);
	while (ftell(file) <= length * 0.2 && !infected)
	{
		fread(&fileChar, sizeof(char), 1, file);
		if (checkFiles(file, sign))
		{
			infected = true;
		}
	}
	if (infected)
	{
		printf("Infected (first 20%%)\n");
		writeIntoFile(logFile, "Infected (first 20%)\n");
		return NULL;
	}
	fseek(file, -1 * (length * 0.2), SEEK_END);
	while (!feof(file) && !infected)
	{
		fread(&fileChar, sizeof(char), 1, file);
		if (checkFiles(file, sign))
		{
			infected = true;
		}
	}
	if (infected)
	{
		printf("Infected (last 20%%)\n");
		writeIntoFile(logFile, "Infected (last 20%%)\n");
		return NULL;
	}
	normalScan(file, sign, logFile);
}

bool checkFiles(FILE* file, FILE* sign)
{
	char signChar = ' ', fileChar = ' ';
	fseek(sign, 1, SEEK_SET);
	while(!feof(sign))
	{
		fread(&signChar, sizeof(char), 1, sign);
		fread(&fileChar, sizeof(char), 1, file);
		if(signChar != fileChar)
		{
			return false;
		}
	}
	return true;
}
