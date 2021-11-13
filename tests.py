query = "Молоко сухое Сухое молоко"
long_query = query.split(' ')[1].title() + " " + query.split(' ')[0].lower()

print(long_query)