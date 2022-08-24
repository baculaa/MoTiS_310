<h1>Multi-Robot Formation</h1>

This program takes in reference goal, size, orientation, and number of robots to formulate a geometric shape which is apart of a larger project. Geometry is one of six parameters in a a framework named MOTIS to enable easier design of multi-robot expressive motion.

In this documentation, these are the steps of properly using the geometryScript3.0 python program. If there are any questions or inquiries about the program, please do not hesitate to contact me at my email: ethan.villalovoz@gmail.com. With that out of the way let's begin.

<h2>Key Terms:</h2>

1. Reference X goal: The robot will be seen on a 2D plane. This is the “origin” which the robot will be placed upon based on the other inputs. This is specifically the X coordinate.
2. Reference Y goal: The robot will be seen on a 2D plane. This is the “origin” which the robot will be placed upon based on the other inputs. This is specifically the Y coordinate.
3. Radius/length: Self explanatory, just wants the size of the shape.
4. Number of robots: Self explanatory; however, must keep in mind that some shapes have different constraints for the minimum required robots.
5. Orientation of shape: Must enter in degrees, will rotate the shape based on that.

<h2>Getting Started:</h2>

1. First, begin running the program. Once you start running the program, you will immediately be prompted to select from the various shapes.
<img width="979" alt="Screen Shot 2022-08-09 at 12 14 26 PM" src="https://user-images.githubusercontent.com/110315314/183742994-c2790a0f-7c30-474d-b450-be8dd61e860a.png">

2. To properly enter a valid input, you must type the name of the shape you want. You do not need to worry about capitalization of any of the letters; however, having a space at the end of input or not including the dash (-) for “semi-circle”, it will continue the program as if you chose line as your input option.

After you choose your wanted shape, you will see this on the console.
<img width="979" alt="Screen Shot 2022-08-09 at 12 14 54 PM" src="https://user-images.githubusercontent.com/110315314/183743462-b61c8099-e5f5-43b1-9216-b80ea1b75d17.png">

3. You will be asked to enter information in this order: reference X goal, reference Y goal, radius/length, number of robots, and orientation of shape. 

With knowing the information now, you must enter them as you see in the example above, you must have a comma in between for the program to parse through and store them into an array. 

Ex: 333,34,23,345

Do not have a space in between the commas. The only flag that will occur is if you enter the improper amount of robots. The maximum number of robots you can have is 10, but the minimum will vary.

<img width="979" alt="Screen Shot 2022-08-09 at 12 15 25 PM" src="https://user-images.githubusercontent.com/110315314/183743766-9e952733-df87-4e6a-9f17-bf1b353a412b.png">

As you can see, when I selected a circle, but I entered 2 robots, the program caught me for it and will ask me for a valid number. Enter this and the program will continue.

After this what you will see is all of the final robot positions which they will be around the reference goal.

<img width="979" alt="Screen Shot 2022-08-09 at 12 15 49 PM" src="https://user-images.githubusercontent.com/110315314/183743850-3e56d7aa-af95-45cf-b5f4-32eae6320d20.png">

End of program. If you see in the code any improvements please let me know and I will fix it!

<h2>Debugging:</h2>

In this section, I will be going more in depth of the program from top down. This is to explain what parts of the code could be added/deleted based on your use.

In the beginning of the main function, print statement and input statements there to show what options and ask the user what shape to choose. Other shapes can be asked here for your purpose. Once the user input is chosen, it is stored in the variable *shape* which is then ran through conditionals to determine which function you will enter and passing in the *shape* as a parameter. 

For each of the shape functions, *shape* parameter will be ran into the userInformation function. The function is desgined to grab 5 inputs in this order: Reference X goal, Reference Y goal, length/radius, number of robots, and orientation. X-Coordinate and Y-Coordinate are asked the same for each option *shape* choice, after there are conditional which check the *shape* and enter the conditional to prompt those specific oriented question. As you may, you can take away any of the question you like or add constraints. 
The format required of entering your input is as follows: (X-Coordinate),(Y-Coordinate),(length/radius),(Number of Robots),(Orientation)
The information is then parsed into an array through the comma being a delimiter using this line: [int(x) for x in info.split(',') if x.strip()].
All information will be typecast to an integer and then stored to an index of array starting at the beginning and ending the information at the ,.
As a safe guard, I implemented a while loop that runs continuously to check if the number of robots in the configuration for the respective shape. The maximum amount of robots for each of the shapes is 10. The minimum amount is for square 4 robots, triangle 3 robots, semi-circle 3 robots, clump 3 robots, circle 3 robots, and line 2 robots. Once this is satisfied, the function returns the array.

Now we have the array returned into the shape function you chosen and depending an the shape, you will be prompted with more information to specify the shape configuration. Once that is all done, the calculations for each of the shapes will vary different. Note, where trig function is written it is either cos() or sin() based on the X-coordinate and Y-coordinate.

1. Square: All of the calculations are hardcoded to a specific points of the shape.
2. Triangle: Two lines are created and rotated 45 degrees opposite of each other. Depending on the number of robots, the end point of the triangle is there or removed.
3. Semi-Circle: Adds to the Reference X goal and Reference Y goal: radius * (trig Function(π * j) / (Number of Robots - 1). j being an integer starting at 0 which increments by one for each of the robots.
4. Clump: For the angular option, it is hardcoded with few variables being randomized with arithmetic. For the rounded option, it has a frame of the circle computations, with added arithmetic outside which are randomized.
5. Circle: Adds trigonometric functions to the Reference X goal and Reference Y goal: radius * (trig Function(2 * π * j) / (Number of Robots).
6. Line: Starts from an endpoint and is added equally distance between based on the number of robots. Creates the entire length of the line.

At the end of all the shape functions, it will compute the orientation of the shape based on the user input from earlier before. The Reference X goal and Reference Y goal are used at the origin point and the current robot's X and Y cooridnnates are called to all four being passed into a linear rotation equation function. Once computed, the new coordinates are replaced in the shape array. Returns the array function of the shape.

Now we are back in the main function and based on the length of the array, it prints all of the coordinates for the amount of robots in the configuration.
