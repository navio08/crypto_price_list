# crypto_price_list
This API provides both current and historical prices on the all crypto assets sorted by rank

## Goals
Implement the fastest API possible while having a simple, reliable and resilient infraestructure

## Business Usage
The client was not able to tell what is the business case for this request.

1. Is just an API for crypto prices screening in a website for just visual information?
2. Is it going to be consumed by services that need reliable data at each request?
3. Etc

When *~~developing software~~* solving problems, the *~~developer~~* the engineer needs to fully understand what the client needs, because it is never about what the client wants, but what the client needs.

>The client will always change requirements, but he will never change the idea that underlies all the requirements. That's why the engineer needs to see the Product as a living being and hence develop software as a continuos refactoring iterations.

## Arquitecture
When thinking about the architecture, many questions came to my mind.
- How many requests per second are we expecting? Do I need to return data for every request?
- Is speed what I want to prioritize?
- Will this product be deployed in cloud or in-site?
- How is my product going to evolve? In which direction?


### Shared Database for Current and Historical data
Pros:
- you'll have the latest current price right to send out
- Good scalability

Cons:
- You'll end up creating a Crypo Prices Databases which is the goal of this challenge.
- You are storing more data that you may want. The disk size will grow fast (too fast)
- You need to implement a different logic if the historical price requested is not available. Hence, 2 implementations to mantain
- Many services with I/O operations to the same database

### Publish/Subscriber
Pros:
- you'll just get the info you need in a quick manner
- organic growth in the database disk size
- Good scalability

Cons:
- Adds complexity
- A Message broker will always guarantee the message delivery and this is not needed for this challenge. I'm happy to drop messages here.


### RPC


### HTTP

## The Aggregator Pattern

## Manual to run the code