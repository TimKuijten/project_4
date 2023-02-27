# Restaurant reviews in different languages
![image](https://user-images.githubusercontent.com/121023453/221655099-49b3a661-4609-4534-afd2-a4d400fd5651.png)

The restaurant industry is strongly influenced by customer reviews, as they can have a significant impact on a restaurant's reputation and success. With the increasing globalization and multiculturalism of our society, it is common to see restaurant reviews written in different languages.

In this context, we will explore a dataset containing restaurant reviews in various languages, and investigate whether the language used in reviews affects their tone and ratings. Specifically, we will examine the following hypothesis:

- The language that leaves the lowest rated reviews, also has the most negative sentiment 
- When people leave a review of a cuisine from their own country, they are biased (French - French, Japanese - Japanese)
- Reviews in north-european languages have a more negative tone (Dutch, German, Norwegian, Swedish, Russian)
- Reviews in Asian languages are focused on other things that reviews in European languages. 

### Scraping data 
To get the dataset we used BeautifulSoup to gather almost 20.000 reviews from about 150 restaurants in Barcelona in 22 languages. With almost all languages (except Arabic) being represnted by over 500 reviews. The information we gathered were the restaurant name, the review, the domain of the website the review was taken from and the rating connected to that review.

### Cleaning and enriching data
To make the data more useful, we add a translation of every review. We add the language it was written in, based on the domain of then website where the review came from. And we used MYSQL to join another table we scraped from TripAdvisor which contains more information about the restaurant; the overall rating and the cuisine type. 

### Data vizualisation 
In the graph below we can see on the left the average score given per review for each language, on the right the average compound per review for each language

![image](https://user-images.githubusercontent.com/121023453/221659517-fd16be9f-2b6e-4f3a-9613-77062d7367f2.png)

In the graphic we see that there is no direct relation between the rating and the compound of a review.
We can conclude that reviews in Chinese, Korean and Russian have the most negative sentiment, while they are both average for the actual review score.
While German reviewers are the least eager with giving a high score, the sentiment of German messages scores average.
We can only find a corelation between both with Norwegian and Swedish; they score quite low in both charts. And that reviews in Hindi score the highest over-all and have the most positive sentiment.

Let's take a closer look at the distrubution of ratings per language 

![image](https://user-images.githubusercontent.com/121023453/221661561-e8efe6f5-1138-4744-9bfa-7130a145e816.png)

We see that the rating per language is pretty much distributed in the same way. The only difference we see is that ratings from reviews in Hebrew are a bit higher than the rest.

When we look at the distrubution of the compounds, we see a very different result.

![image](https://user-images.githubusercontent.com/121023453/221661454-130e7591-46d8-42a0-af3f-378052256b3f.png)

We can see that german has many outlayers, and again that Hindi is the most positive when it comes to the compound of reviews.

To answer our second hypothesis; When people leave a review of a cuisine from their own country, they are biased we look at the chart below.

![image](https://user-images.githubusercontent.com/121023453/221667365-728894e8-e054-4e21-a1d3-05ba90bc8046.png)

When looking at this chart we can conclude that the hypositis is true, reviews are biased when reviewing their 'own' cuisine in the matching language. 

![image](https://user-images.githubusercontent.com/121023453/221661561-e8efe6f5-1138-4744-9bfa-7130a145e816.png)

Let's take a look at the most frequently words used in reviews and see if there is a noticable difference between reviews in European languages vs Asian languages.
The image on the left is based on reviews lower than 30, the image on the right is reviews between 35 to 50
# European languages

![image](https://user-images.githubusercontent.com/121023453/221662653-916df457-2738-4b1d-9fd2-3890b324367d.png)

## Asian languages

![image](https://user-images.githubusercontent.com/121023453/221662344-987ffce2-b632-49e6-a8a4-9a87716169b5.png)

There is not really a noticable difference; apart from that it seems that reviews in Asian languages don't have much good to say about pizza.

![image](https://user-images.githubusercontent.com/121023453/221662653-916df457-2738-4b1d-9fd2-3890b324367d.png)

