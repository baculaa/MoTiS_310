<h1>Multi-Robot Formation</h1>

This program takes in reference goal, size, orientation, and number of robots to formulate a geometric shape which is apart of a larger project. Geometry is one of six parameters in a a framework named MOTIS to enable easier design of multi-robot expressive motion.

In this documentation, these are the steps of properly using the geometryScript3.0 python program. If there are any questions or inquiries about the program, please do not hesitate to contact me at my email: ethan.villalovoz@gmail.com. With that out of the way let's begin.

<h2>Getting Started:</h2>

Once you start running the program, you will immediately be prompted to select from the various shapes.
<img width="979" alt="Screen Shot 2022-08-09 at 12 14 26 PM" src="https://user-images.githubusercontent.com/110315314/183742994-c2790a0f-7c30-474d-b450-be8dd61e860a.png">

To properly enter a valid input, you must type the name of the shape you want. You do not need to worry about capitalization of any of the letters; however, having a space at the end of input or not including the dash (-) for “semi-circle”, it will continue the program as if you chose line as your input option.

After you choose your wanted shape, you will see this on the console.
<img width="979" alt="Screen Shot 2022-08-09 at 12 14 54 PM" src="https://user-images.githubusercontent.com/110315314/183743462-b61c8099-e5f5-43b1-9216-b80ea1b75d17.png">

You will be asked to enter information in this order: reference X goal, reference Y goal, radius/length, number of robots, and orientation of shape. Below I will describe each of the inputs:

1. Reference X goal: The robot will be seen on a 2D plane. This is the “origin” which the robot will be placed upon based on the other inputs. This is specifically the X coordinate.
2. Reference Y goal: The robot will be seen on a 2D plane. This is the “origin” which the robot will be placed upon based on the other inputs. This is specifically the Y coordinate.
3. Radius/length: Self explanatory, just wants the size of the shape.
4. Number of robots: Self explanatory; however, must keep in mind that some shapes have different constraints for the minimum required robots.
5. Orientation of shape: Must enter in degrees, will rotate the shape based on that.

With knowing the information now, you must enter them as you see in the example above, you must have a comma in between for the program to parse through and store them into an array. 

Ex: 333,34,23,345

Do not have a space in between the commas. The only flag that will occur is if you enter the improper amount of robots. The maximum number of robots you can have is 10, but the minimum will vary.

<img width="979" alt="Screen Shot 2022-08-09 at 12 15 25 PM" src="https://user-images.githubusercontent.com/110315314/183743766-9e952733-df87-4e6a-9f17-bf1b353a412b.png">

As you can see, when I selected a circle, but I entered 2 robots, the program caught me for it and will ask me for a valid number. Enter this and the program will continue.

After this what you will see is all of the final robot positions which they will be around the reference goal.

<img width="979" alt="Screen Shot 2022-08-09 at 12 15 49 PM" src="https://user-images.githubusercontent.com/110315314/183743850-3e56d7aa-af95-45cf-b5f4-32eae6320d20.png">

End of program. If you see in the code any improvements please let me know and I will fix it!

<h1>Debugging:</h1>

Part of code to go more indepth on changing what to do.
Top down run through 

