import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Movie:
    def __init__(self, user):
        self.user = user
        self.num_users, self.num_movies = user.shape
        self.user_similarity()

    def user_similarity(self):
        self.user_similarity = cosine_similarity(self.user)

    def make_movie_recommendations(self, user_id, num_recommendations):
        similar_users = self.user_similarity[user_id].argsort()[::-1][1:]
        unrated_movies = np.where(self.user[user_id] == 0)[0]
        movie_scores = np.sum(self.user[similar_users][:, unrated_movies] * self.user_similarity[user_id][similar_users][:, np.newaxis], axis=0)
        recommended_movies = unrated_movies[np.argsort(movie_scores)[::-1]][:num_recommendations]
        return recommended_movies

user = np.array([[5, 3, 0, 1],
                 [4, 0, 0, 1],
                 [1, 1, 0, 5],
                 [1, 0, 0, 4]])

movie_names = ['Hacked', 'Badlapur', 'Gangs of wasseypur', 'Article 15', 'Pushpa', 'Drishyam']
movie_cf = Movie(user)
user_id = int(input("Enter user id (PLEASE ENTER THE USER ID B/W O TO 3): "))
num_recommendations = 3
recommendations = movie_cf.make_movie_recommendations(user_id, num_recommendations)

recommended_movies = [movie_names[movie_id] for movie_id in recommendations]

print("Movie Recommendations for User {}: {}".format(user_id, recommended_movies))