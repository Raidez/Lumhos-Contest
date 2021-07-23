extends Node2D

const Firefly = preload("res://Firefly.tscn")

export var nb: int = 100

################################################################################

func _ready():
	for i in range(nb):
		var firefly = Firefly.instance()
		add_child(firefly)
