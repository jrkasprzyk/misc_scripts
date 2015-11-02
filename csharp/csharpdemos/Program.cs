using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace csharpdemos
{
    public static class MyFunctionSet
    {
        public static double AddTwoNumbers(double a, double b)
        {
            return a + b;
        }

        public static double SubtractTwoNumbers(double a, double b)
        {
            return a - b;
        }
    }

    class Car
    {
        //variable declarations
        private string color;
        private string make;
        private string model;

        //constructor
        public Car(string color, string make, string model)
        {
            this.color = color;
            this.make = make;
            this.model = model;
        }

        //properties
        public string Color
        {
            get { return color; }
            set
            {
                Console.WriteLine("The car is " + color + " its color cannot be changed to " + value + "!");
            }
        }

        public string Make
        {
            get { return make; }
            set { make = value; }
        }

        //functions
        public string Describe()
        {
            return "This is a " + color + " " + make + " " + model + "!";
        }

        public void Paint(string newColor)
        {
            this.color = newColor;
            return;
        }
    }

    class Program
    {
        static void EnterOneName()
        {
            string firstName = "John";
            string lastName = "Doe";
            int age;

            //writing and reading from the console
            Console.WriteLine("Default Name: " + firstName + " " + lastName);


            Console.WriteLine("Please enter a new first name:");
            firstName = Console.ReadLine();
            Console.WriteLine("Please enter a new last name:");
            lastName = Console.ReadLine();

            Console.WriteLine("New name: " + firstName + " " + lastName);

            Console.WriteLine("Now enter an age");
            age = int.Parse(Console.ReadLine());

            Console.WriteLine(firstName + " " + lastName + " is " + age + " years old.");

            if (age > 50)
                Console.WriteLine("That motherfucker is old isn't he?");
            else
                Console.WriteLine("I guess he isn't that old, is he.");
            return;
        }
        static void SpittingOutNumbers()
        {
            Console.WriteLine("Enter an integer number.");
            int myNumber;
            int myCounter = 0;
            myNumber = int.Parse(Console.ReadLine());
            Console.WriteLine("You entered " + myNumber + ". It's a good one. Let's count up to it!");

            while (myCounter < myNumber)
            {
                Console.WriteLine("Number " + myCounter);
                myCounter++;
            }
            return;
        }

        static int AddFivetoThis(ref int input)
        {
            // the ref keyword passes the input by reference, so that
            // the value of it remains even outside of the function
            input = input + 5;
            return input;
        }

        static void EnterMultipleNames()
        {
            Console.WriteLine("Enter how many names you'd like:");

            int numberOfNames = int.Parse(Console.ReadLine());
            string[] names;
            names = new string[numberOfNames];

            Console.WriteLine("Now enter them, typing an enter after each.");

            for (int i = 0; i < numberOfNames; i++)
                names[i] = Console.ReadLine();

            Console.WriteLine("The names you entered are:");
            foreach (string name in names)
                Console.WriteLine(name);

        }



        static void CarTester()
        {
            Car sarahsCar;
            sarahsCar = new Car("white", "Ford", "Focus");

            Car emilsCar;
            emilsCar = new Car("gray", "Mercury", "Cougar");

            Console.WriteLine(emilsCar.Describe());
            Console.WriteLine("Trying to call the set color property...");
            emilsCar.Color = "purple";

            Console.WriteLine("Now, showing the new function I wrote to change color...");
            emilsCar.Paint("purple");

            Console.WriteLine("The make of Emils car is" + emilsCar.Make + ".");

            Console.WriteLine("Changing the make...");
            emilsCar.Make = "Ford";

            Console.WriteLine(emilsCar.Describe());

            return;
        }

        static void Main(string[] args)
        {
            //EnterOneName();
            //SpittingOutNumbers();

            //int tester = 2;
            //AddFivetoThis(ref tester);

            //EnterMultipleNames();

            double a = 30.0;
            double b = 20.0;
            double c = MyFunctionSet.AddTwoNumbers(a, b);
            Console.WriteLine(a + " plus " + b + " is " + c);

            CarTester();

            Console.WriteLine("Hit enter to end...");
            Console.ReadLine();
            return;
        }
    }
}
