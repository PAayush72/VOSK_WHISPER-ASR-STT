// let student = {
//   name: "Aayush",
//   marks: {
//     math: 85,
//     science: 90
//   }
// };

// console.log(` ${student.name} scored ${student.marks.science} in  ${Object.keys(student.marks)[1]} ` );


// let car = {
//   brand: "Toyota",
//   model: "Innova",
//   year: 2020
// };

// // add property: color = "white"
// car.color = "white"

// // delete property: year
// delete car.year

// // print final object
// console.log(car)


// let user = {
//   name: "John",
//   email: "john@gmail.com"
// };

// // check if "phone" exists in user
// console.log('phone' in user)
// // print true or false


// let employees = [
//   { name: "A", salary: 20000 },
//   { name: "B", salary: 30000 },
//   { name: "C", salary: 25000 }
// ];

// // print names of employees whose salary > 25000
// for(let emp of employees){
//     if(emp.salary>25000)
//     {
//         console.log(emp.name)
//     }
// }


// let products = [
//   { id: 1, name: "Mobile", price: 12000 },
//   { id: 2, name: "Laptop", price: 55000 },
//   { id: 3, name: "Mouse", price: 500 }
// ];

// let total= 0;
// // calculate total price using loop
// for(let p of products){
//     total = total+p.price
// }
// console.log(total)


// let users = [
//   { name: "Raj", age: 17 },
//   { name: "Amit", age: 21 },
//   { name: "Neha", age: 19 }
// ];

// // print names of users who are eligible to vote
// for(let u of users){
//     if(u.age>18){
//         console.log(u.name)
//     }
// }


// let personal = { name: "Aayush", age: 22 };
// let professional = { role: "Developer", company: "ABC" };

// // merge both objects into one
// let mer = {...personal,...professional}
// console.log(mer)

// console.log(Object.assign(personal,professional))


// let original = { a: 1, b: 2 };
// console.log(original)
// let copy = original;

// // change copy.a = 100
// copy.a = 100
// // print original
// console.log(original,copy)
// // explain output



// let obj = { x: 10, y: 20 };

// // create a new object with z = 30 using spread
// let newobj ={
//     ...obj,
//     z:30
// }
// console.log(newobj)


// let user = {
//   name: "John",
//   address: {
//     city: "Delhi"
//   }
// };

// let newUser = { ...user };
// newUser.address.city = "Mumbai";

// console.log(user.address.city);
// // what will be output and why?


// let data = {
//   id: 1,
//   info: {
//     name: "Phone",
//     price: 10000
//   }
// };

// // print price safely using optional chaining
// console.log(data.price)

let scores = [10, 20, 30];

// print max value WITHOUT using Math.max
let a=0,b=0;
for(val in scores){
    a>b?a:b
}