def printattr(objects, attr):
	objects.sort(key=lambda x: x.id)
	for i in objects:
		print(i, getattr(i, attr))