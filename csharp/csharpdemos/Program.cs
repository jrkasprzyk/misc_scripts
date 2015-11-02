using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

/// <summary>
/// Playing around with the tutorial here: http://csharp.net-tutorials.com/classes/inheritance/
/// </summary>

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
        protected string color;
        protected string make;
        protected string model;

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
        public virtual string Describe()
        {
            return "This is a " + color + " " + make + " " + model + "!";
        }

        public void Paint(string newColor)
        {
            this.color = newColor;
            return;
        }
    }

    class SportsCar : Car
    {
        private string seatType;

        public SportsCar(string color, string make, string model, string seatType) : base(color, make, model)
        {
            this.seatType = seatType;
        }

        public string SeatType
        {
            get
            {
                return seatType;
            }
            set { this.seatType = value;  }
        }

        public override string Describe()
        {
            return "This is a " + color + " " + make + " " + model + ". Since its a sports car it also has " + seatType + " seats!";
        }

    }

    public static class AsyncTestbed
    {
        //https://msdn.microsoft.com/en-us/library/hh191443.aspx
        public static async Task<int> AccessTheWebAsync()
        {
            HttpClient client = new HttpClient();

            //do the below task asynchronously
            Console.WriteLine("Launching asynchronous task!");
            Task<string> getStringTask = client.GetStringAsync("http://www.wsj.com/");

            //do some work
            long N = 100000;
            long junk = 0;
            for (long i = 0; i < N; i++)
            {
                junk += i*N;
                junk = junk / 25;
            }
            Console.WriteLine("We are done doing that stupid work and the value of the variable is " + junk);

            // The await operator suspends AccessTheWebAsync.
            //  - AccessTheWebAsync can't continue until getStringTask is complete.
            //  - Meanwhile, control returns to the caller of AccessTheWebAsync.
            //  - Control resumes here when getStringTask is complete. 
            //  - The await operator then retrieves the string result from getStringTask.
            string urlContents = await getStringTask;
            //Console.WriteLine("String task received, its contents are" + urlContents);

            return urlContents.Length;

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

            Console.WriteLine("After calling the Paint method we have...");
            Console.WriteLine(emilsCar.Describe());

            Console.WriteLine("Changing the make...");
            emilsCar.Make = "Ford";

            Console.WriteLine(emilsCar.Describe());

            SportsCar joesCar;
            joesCar = new SportsCar("red", "Nissan", "Sentra", "leather");
            Console.WriteLine(joesCar.Describe());

            return;
        }

        static void Main(string[] args)
        {
            //EnterOneName();
            //SpittingOutNumbers();

            //int tester = 2;
            //AddFivetoThis(ref tester);

            //EnterMultipleNames();

            //double a = 30.0;
            //double b = 20.0;
            //double c = MyFunctionSet.AddTwoNumbers(a, b);
            //Console.WriteLine(a + " plus " + b + " is " + c);

            //CarTester();

            Task<int> n = AsyncTestbed.AccessTheWebAsync();

            Console.WriteLine("n = " + n);

            Console.WriteLine("Hit enter to end...");
            Console.ReadLine();
            return;
        }
    }
}
