#import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

respone = requests.get("https://content.codecademy.com/courses/beautifulsoup/cacao/index.html")

webpage = respone.text
soup = BeautifulSoup(webpage, "html.parser")
rating_tags = soup.find_all(attrs={"class":"Rating"})

ratings = []
for rating in rating_tags[1:]:
  rating = float(rating.get_text())
  ratings.append(rating)
plt.hist(ratings)
plt.show()

company_tag = soup.select(".Company")
companies =[]
for company in company_tag[1:]:
  companies.append(company.get_text())


cocoa_tags = soup.select(".CocoaPercent")
cocoas = []
for cocoa in cocoa_tags[1:]:
  cocoas.append(cocoa.get_text().strip('%'))


d = {"Company":companies, "Rating":ratings, "CocoaPercentage":cocoas}
df = pd.DataFrame.from_dict(d)
df.to_csv("Chocolate.csv", index = False)
mean_ratings = df.groupby("Company").Rating.mean()
ten_best = mean_ratings.nlargest(10)
print(ten_best)

plt.clf()
plt.scatter(df.CocoaPercentage, df.Rating)

z = np.polyfit(df.CocoaPercentage, df.Rating, 1)
line_function = np.poly1d(z)
plt.plot(df.CocoaPercentage, line_function(df.CocoaPercentage), "r--")

plt.show()