# Simple Factory Pattern

The simple factory pattern is a creational design pattern that provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created. In other words, the simple factory pattern delegates the responsibility of object creation to a separate class, called factory, which decides which concrete class to instantiate based on certain conditions or parameters.
So it's quite different (and simpler) compared to the factory method.

Continuing with the logistics example, we could have a `TransportVehicleFactory` class that is ONLY responsible for creating instances of `Truck`, `Ship`, and `Airplane` based on certain conditions or parameters.
Consequently, the constructor of `TransportVehicleFactory` could simply take a parameter indicating which type of transport vehicle to create, have a giant switch-case or if-else that decides which concrete class to instantiate, and return the created instance. This way, if in the future we need to introduce a new concrete class, we just need to add a new condition to the `create()` method of the Factory class, without having to modify our main code.

## Limitations
The simple factory pattern is simple to implement and can be useful in situations where the object creation logic is relatively simple and doesn't require great flexibility. However, it has some limitations:
- If the object creation logic becomes complex, the factory class can become difficult to maintain and test.
- If the number of concrete classes grows, the factory class can become a "god class" that knows all concrete classes, violating the Open/Closed principle.
- It doesn't support extension well, since every time a new concrete class is added, it's necessary to modify the factory class, which can lead to errors and make the code less maintainable.
- It's not suitable for situations where object creation requires complex logic or depends on many variables, since the factory class could become too complicated and difficult to manage.