/* Uses JSONLoader to load objects that have been saved
 * in three.js's json format.  Requires the folder models-json
 * that contains the seven sample models.
 */

var renderer;
// A three.js WebGL or Canvas renderer.
var scene;
// The 3D scene that will be rendered, containing the model.
var camera;
// The camera that takes the picture of the scene.

var model;
// The three.js object that represents the model.

var rotateX = 0;
// rotation of model about the x-axis
var rotateY = 0;
// rotation of model about the y-axis

/*  This function is called by the init() method.  It simply adds
 *  a light to the scene.  Objects are added later by the loader callback.
 */
var mouseDown = false, mouseX = 0, mouseY = 0;

function onMouseMove(evt) {
	if (!mouseDown) {
		return;
	}

	evt.preventDefault();

	var deltaX = evt.clientX - mouseX, deltaY = evt.clientY - mouseY;
	mouseX = evt.clientX;
	mouseY = evt.clientY;
	rotateScene(deltaX, deltaY);
}

function onMouseDown(evt) {
	evt.preventDefault();

	mouseDown = true;
	mouseX = evt.clientX;
	mouseY = evt.clientY;
}

function onMouseUp(evt) {
	evt.preventDefault();

	mouseDown = false;
}

function addMouseHandler(canvas) {
	canvas.addEventListener('mousemove', function(e) {
		onMouseMove(e);
	}, false);
	canvas.addEventListener('mousedown', function(e) {
		onMouseDown(e);
	}, false);
	canvas.addEventListener('mouseup', function(e) {
		onMouseUp(e);
	}, false);
}

function rotateScene(deltaX, deltaY) {
	root.rotation.y += deltaX / 100;
	root.rotation.x += deltaY / 100;
}

function createWorld() {
	var light;
	// A light shining from the direction of the camera.
	light = new THREE.DirectionalLight();
	light.position.set(0, 0, 1);
	scene.add(light);
}

/**
 * The callback function that is called by the JSONLoader when it
 * has finished loading the object.  This function creates a three.js
 * function to hold the object.  It translates the object so that
 * its center is in the origin.  It wraps the object in another object
 * that is used to scale and rotate the object.  The scale is set
 * so that the maximum coordinate in its vertices, in absolute
 * value, is scaled to 10.  The rotation is controlled by the arrow
 * keys.
 */
function modelLoadedCallback(geometry, materials) {

	/* create the object from the geometry and materials that were loaded.  There
	 can be multiple materials, which can be applied to the object using MeshFaceMaterials.
	 Note tha the material can include references to texture images might finish
	 loading later. */

	var object = new THREE.Mesh(geometry, new THREE.MeshFaceMaterial(materials));

	/* Determine the ranges of x, y, and z in the vertices of the geometry. */

	var xmin = Infinity;
	var xmax = -Infinity;
	var ymin = Infinity;
	var ymax = -Infinity;
	var zmin = Infinity;
	var zmax = -Infinity;
	for (var i = 0; i < geometry.vertices.length; i++) {
		var v = geometry.vertices[i];
		if (v.x < xmin)
			xmin = v.x;
		else if (v.x > xmax)
			xmax = v.x;
		if (v.y < ymin)
			ymin = v.y;
		else if (v.y > ymax)
			ymax = v.y;
		if (v.z < zmin)
			zmin = v.z;
		else if (v.z > zmax)
			zmax = v.z;
	}

	/* translate the center of the object to the origin */
	var centerX = (xmin + xmax) / 2;
	var centerY = (ymin + ymax) / 2;
	var centerZ = (zmin + zmax) / 2;
	var max = Math.max(centerX - xmin, xmax - centerX);
	max = Math.max(max, Math.max(centerY - ymin, ymax - centerY));
	max = Math.max(max, Math.max(centerZ - zmin, zmax - centerZ));
	var scale = 10 / max;
	object.position.set(-centerX, -centerY, -centerZ);
	console.log("Loading finished, scaling object by " + scale);
	console.log("Center at ( " + centerX + ", " + centerY + ", " + centerZ + " )");
	/* Create the wrapper, model, to scale and rotate the object. */

	model = new THREE.Object3D();
	model.add(object);
	model.scale.set(scale, scale, scale);
	
	rotateX = rotateY = 0;
	model.overdraw = true;
	scene.add(model);
	render();	

}
/**
 * Called when the setting of the model-selection radio buttons is changed.
 * starts loading the model from the specified file and sets the background
 * color for the renderer (since black background doesn't work for all
 * of the models.
 */
function installModel(file, bgColor) {
	if (model) {
		scene.remove(model);
	}
	renderer.setClearColor(0x000000, 0);
	renderer.AA = 1;
	render();
	var loader = new THREE.JSONLoader();
	loader.load('/home/ikarus_app/web/projecte_final_daw/ikarus_base/static/' + file, modelLoadedCallback);
}

/**
 *  The render fucntion creates an image of the scene from the point of view
 *  of the camera and displays it in the canvas.  This is called at the end of
 *  init() to produce the initial view of the model, and it is called each time
 *  the user presses an arrow key, return, or home.
 */
function render() {
	renderer.render(scene, camera);
}

/**
 *  An event listener for the keydown event.  It is installed by the init() function.
 */
function doKey(evt) {
	var rotationChanged = true;
	switch (evt.keyCode) {
		case 37:
			rotateY -= 0.05;
			break;
		// left arrow
		case 39:
			rotateY += 0.05;
			break;
		// right arrow
		case 38:
			rotateX -= 0.05;
			break;
		// up arrow
		case 40:
			rotateX += 0.05;
			break;
		// down arrow
		case 13:
			rotateX = rotateY = 0;
			break;
		// return
		case 36:
			rotateX = rotateY = 0;
			break;
		// home
		default:
			rotationChanged = false;
	}
	if (model && rotationChanged) {
		model.rotation.set(rotateX, rotateY, 0);
		render();
		evt.preventDefault();
	}
}
/**
 *  This function is called by the onload event so it will run after the
 *  page has loaded.  It creates the renderer, canvas, and scene objects,
 *  calls createWorld() to add objects to the scene, and renders the
 *  initial view of the scene.  If an error occurs, it is reported.
 */
function init() {

	try {
		var theCanvas = document.getElementById("cnvs");
		if (!theCanvas || !theCanvas.getContext) {
			document.getElementById("message").innerHTML = "Sorry, your browser doesn't support canvas graphics.";
			return;
		}
		try {// try to create a WebGLRenderer
			if (window.WebGLRenderingContext) {
				renderer = new THREE.WebGLRenderer({
					precision : "highp",
					canvas : theCanvas,
					antialias : true,
					alpha : true,
				});
				renderer.setClearColor(0x000000, 0);
			}
		} catch (e) {
		}
		if (!renderer) {// If the WebGLRenderer couldn't be created, try a CanvasRenderer.
			renderer = new THREE.CanvasRenderer({
				precision : "highp",
				canvas : theCanvas,
				antialias : true,
				alpha : true
			});
			renderer.setSize(theCanvas.width, theCanvas.height);
			document.getElementById("message").innerHTML = "WebGL not available; falling back to CanvasRenderer.";
		}
		scene = new THREE.Scene();
		camera = new THREE.PerspectiveCamera(50, theCanvas.width / theCanvas.height, 0.1, 100);
		camera.position.z = 30;
		createWorld();
		installModel("objects/Azwarius.js");
		render();
		document.addEventListener("keydown", doKey, false);
		//document.getElementById("r1").checked = true;
	} catch (e) {
		document.getElementById("message").innerHTML = "Sorry, an error occurred: " + e;
	}
	
}
