import os
import csv
import filecmp
import datetime

def getData(file):
#Input: file name
#Ouput: return a list of dictionary objects where 
#the keys will come from the first row in the data.

#Note: The column headings will not change from the 
#test cases below, but the the data itself will 
#change (contents and size) in the different test 
#cases.

	#Your code here:
	with open(file) as csvfile:
		info_list = list()
		#dict of information
		info_dict = csv.DictReader(csvfile)
		for row in info_dict:
			dict = {}
			dict['First'] = row['First']
			dict['Last'] = row['Last']
			dict['Email'] = row['Email']
			dict['Class'] = row['Class']
			dict['DOB'] = row['DOB']
			info_list.append(dict)

	return info_list


#Sort based on key/column
def mySort(data,col):
#Input: list of dictionaries
#Output: Return a string of the form firstName lastName

	#sorts the list using 'col' input as  the key to sort by
	sorted_list = sorted(data, key=lambda x: x[col])

	return sorted_list[0]['First'] + ' ' + sorted_list[0]['Last']

#Create a histogram
def classSizes(data):
# Input: list of dictionaries
# Output: Return a list of tuples ordered by
# ClassName and Class size, e.g 
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

	#Your code here:
	tuple_count = list()
	size_dict = {}

	for dict in data:
		for key in dict:
			if key == 'Class':
				#creates dictionary that counts how many students are in each year
				if dict[key] not in size_dict:
					size_dict[dict[key]] = 1
				else:
					size_dict[dict[key]] += 1

	#creates a list of tuples from that dictionary
	for key, value in size_dict.items():
		tuple_count.append((key, value))

	#sorts the list by class
	sorted_list = sorted(tuple_count, key=lambda x: x[0])
	#sorts the list by number of students
	final_list = sorted(sorted_list, key=lambda x: x[1], reverse=True)

	return final_list




# Find the most common day of the year to be born
def findDay(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB
	date_count = {}
	tuple_count = list()

	for dict in a:
		for key in dict:
			if key == 'DOB':
				dob = dict[key]
				index_start = dob.find('/') + 1
				day_on = dob[index_start:]
				index_end = day_on.find('/')
				day = day_on[:index_end]
				#creates dictionary where day of month is key and frequency is the value
				if day not in date_count:
					date_count[day] = 1
				else:
					date_count[day] += 1

	#creates list of tuples using the dictionary
	for key, value in date_count.items():
		tuple_count.append((key, value))
	sorted_list = sorted(tuple_count, key=lambda x: x[1], reverse=True)

	return int(sorted_list[0][0])





# Find the average age (rounded) of the Students
def findAge(a):
# Input: list of dictionaries
	total_age = 0.0
	count = 0

	for dict in a:
		bday_string = dict['DOB']
		bday_object = datetime.datetime.strptime(bday_string, '%m/%d/%Y')
		current = datetime.date.today()
		subtract_1 = ((float(current.month), float(current.day)) < (float(bday_object.month), float(bday_object.day)))
		#accounts for future birthdays
		if bday_object.year > 2017:
			age = 0
		else:
			age = float(current.year) - float(bday_object.year) - subtract_1
		total_age += age
		count += 1.0

	average = (total_age) / count
	return int(average)

	


#Similar to mySort, but instead of returning single
#Student, all of the sorted data is saved to a csv file.
def mySortPrint(a,col,fileName):
#Input: list of dictionaries, key to sort by and output file name
#Output: None

	sorted_list = sorted(a, key=lambda x: x[col])

	with open(fileName, 'w') as output:
	 	for dict in sorted_list:
	 		input_string = dict['First'] + ',' + dict['Last'] + ',' + dict['Email'] + ',' + '\n'
	 		output.write(input_string)


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)
	
	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()
