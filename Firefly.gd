extends Node2D

onready var SIZE = get_viewport_rect().size
onready var tween = $Tween
const SPEED = [10, 50]
const BRIGHT = Color8(173, 255, 0)
const DARKER = Color8(26, 36, 7)

var color = DARKER

var radius = rand_range(4, 7)
var speed = rand_range(SPEED[0], SPEED[1])
var countdown = rand_range(1, 5)
var timer = rand_range(0, countdown)
var is_shaked = false

################################################################################

func _ready():
	# position aléatoire de la luciole et de sa cible
	$Body.position.x = rand_range(0, SIZE.x)
	$Body.position.y = rand_range(0, SIZE.y)
	find_new_target()
	
	$Body/Hitbox.shape.radius = radius # mise à jour de la taille de la collision de la luciole
	
	# création de l'animation
	tween.interpolate_property(self, "color", BRIGHT, DARKER, countdown, Tween.TRANS_LINEAR, Tween.EASE_OUT)
	tween.seek(timer)

func _process(delta):
	if is_shaked:
		# la luciole est agitée par le clique
		color = BRIGHT
	else:
		# animation de la couleur
#		old_animation_color(delta)
		tween.start()
	
	# calcul de la nouvelle position pour atteindre la cible
	var angle = atan2($Target.position.y - $Body.position.y, $Target.position.x - $Body.position.x)
	$Body.position.x += speed * delta * cos(angle)
	$Body.position.y += speed * delta * sin(angle)
	
	update() # force le moteur a redessiner à chaque frame


func _draw():
	draw_circle($Body.position, radius, color)

################################################################################

func find_new_target():
	$Target.position.x = rand_range(0, SIZE.x)
	$Target.position.y = rand_range(0, SIZE.y)


func _on_Target_area_entered(area):
	if area != $Body:
		return
	find_new_target()

func old_animation_color(delta):
	# gestion du timer pour changer la couleur
	timer += delta
	if timer > countdown:
		timer -= countdown
	
	# changement de la couleur
	var step = timer / countdown
	color = lerp(BRIGHT, DARKER, step)
