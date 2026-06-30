using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class FlockSimulation : MonoBehaviour {

    public float timeStep = 0.1f;

    private Flock flock;

    private Flock school;

    public Button update;
    public Button scatterBtn;
    public InputField collisionBox;
    public InputField wanderingBox;
    public InputField centeringBox;
    public InputField velocitymBox;
    public InputField collisionRadius;
    public InputField wanderingRadius;
    public InputField centeringRadius;
    public InputField velocitymRadius;
    public InputField deltaTime;
    public Slider numBoid;
    public Toggle wandering;
    public Toggle centering;
    public Toggle velocitym;
    public Toggle collision;
    public Toggle trail;

	// Use this for initialization
	void Start () {
		flock = new Flock(100);

        school = new Flock(0);
        school.wings = false;
        school.yMin = -30f;
        school.yMax = -10f;
        school.generateFlock(50);
        
        GameObject ocean = GameObject.CreatePrimitive(PrimitiveType.Cube);
        ocean.transform.position = new Vector3(0, -20f, 0);
        ocean.transform.localScale = new Vector3(110f, 30f, 110f);
        Material material = new Material(Shader.Find("Transparent/Diffuse"));
        material.color = new Color(0f, 0f, 0.8f, 0.3f);
        ocean.GetComponent<Renderer>().material = material;

        scatterBtn = GameObject.Find("scatter").GetComponent<Button>();
        scatterBtn.onClick.AddListener(scatter);

        update = GameObject.Find("update").GetComponent<Button>();
        update.onClick.AddListener(guiUpdate);

        collisionBox = GameObject.Find("collisionBox").GetComponent<InputField>();
        collisionBox.text = "3.0";
        wanderingBox = GameObject.Find("wanderingBox").GetComponent<InputField>();
        wanderingBox.text = "5.0";
        centeringBox = GameObject.Find("centeringBox").GetComponent<InputField>();
        centeringBox.text = "1.0";
        velocitymBox = GameObject.Find("velocitymBox").GetComponent<InputField>();
        velocitymBox.text = "0.3";
        collisionRadius = GameObject.Find("collisionRadius").GetComponent<InputField>();
        collisionRadius.text = "1.0";
        centeringRadius = GameObject.Find("centeringRadius").GetComponent<InputField>();
        centeringRadius.text = "20.0";
        velocitymRadius = GameObject.Find("velocitymRadius").GetComponent<InputField>();
        velocitymRadius.text = "100.0";
        deltaTime = GameObject.Find("deltaTime").GetComponent<InputField>();
        deltaTime.text = "0.1";
        wandering = GameObject.Find("wandering").GetComponent<Toggle>();
        centering = GameObject.Find("centering").GetComponent<Toggle>();
        velocitym = GameObject.Find("velocitym").GetComponent<Toggle>();
        collision = GameObject.Find("collision").GetComponent<Toggle>();
        numBoid = GameObject.Find("numBoid").GetComponent<Slider>();
        numBoid.value = 100;
        trail = GameObject.Find("trail").GetComponent<Toggle>();
        trail.isOn = false;
	}
	
	// Update is called once per frame
	void Update () {
		flock.update(timeStep);
        school.update(timeStep);
        
        if (Input.GetKeyDown("space"))
            scatter();
	}

    void guiUpdate() {
        flock.generateFlock((int)numBoid.value);
        if (wandering.isOn) {
            flock.wanderingWeight = float.Parse(wanderingBox.text);
        } else {
            flock.wanderingWeight = 0f;
        }
        if (collision.isOn) {
            flock.collisionWeight = float.Parse(collisionBox.text);
            flock.collisionRadius = float.Parse(collisionRadius.text);
        } else {
            flock.collisionWeight = 0f;
        }
        if (velocitym.isOn) {
            flock.velocitymWeight = float.Parse(velocitymBox.text);
            flock.velocitymRadius = float.Parse(velocitymRadius.text);
        } else {
            flock.velocitymWeight = 0f;
        }
        if (centering.isOn) {
            flock.centeringWeight = float.Parse(centeringBox.text);
            flock.centeringRadius = float.Parse(centeringRadius.text);
        } else {
            flock.centeringWeight = 0f;
        }
        flock.trailOn = trail.isOn;

        timeStep = float.Parse(deltaTime.text);
    }

    void scatter() {
        flock.scatterFlock();
    }
}
