using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Flock {

    public Boid[] boids;

    public Vector3 centroid;

    public int numBoids = 0;

    public float wanderingWeight = 5.0f;
    public float centeringWeight = 1.0f;
    public float collisionWeight = 3.0f;
    public float velocitymWeight = 0.3f;

    public float centeringRadius = 20f;
    public float collisionRadius = 1f;
    public float velocitymRadius = 1000f;

    public float xMin = -50f;
    public float xMax = 50f;
    public float zMin = -50f;
    public float zMax = 50f;
    public float yMin = 0f;
    public float yMax = 20f;

    public float minVel = 1f;
    public float maxVel = 15f;

    public float trailTime = 3f;
    public bool trailOn = false;

    public bool wings = true;

	public Flock(int n) {
        generateFlock(n);
    }
	
	// Update is called once per frame
	public void update(float timeStep) {
        for (int i = 0; i < numBoids; i++) {
            boids[i].update(this, timeStep);
        }
	}

    public void generateFlock(int n) {
        Boid[] newBoids = new Boid[n];

        if (n > numBoids) {
            for (int i = 0; i < numBoids; i++) {
                newBoids[i] = boids[i];
            }

            for (int i = numBoids; i < n; i++) {
                newBoids[i] = getBoid();
            }
        } else {
            for (int i = 0; i < n; i++) {
                newBoids[i] = boids[i];
            }

            for (int i = n; i < numBoids; i++) {
                UnityEngine.Object.Destroy(boids[i].gameObj);
            }
        }

        numBoids = n;
        boids = newBoids;
    }
    
    public void scatterFlock() {
        for (int i = 0; i < numBoids; i++) {
            float x = Random.value * (xMax - xMin) + xMin;
            float y = Random.value * (yMax - yMin) + yMin;
            float z = Random.value * (zMax - zMin) + zMin;
            boids[i].position = new Vector3(x, y, z);
        }
    }

    public Boid getBoid() {
        float x = Random.value * (xMax - xMin) + xMin;
        float y = Random.value * (yMax - yMin) + yMin;
        float z = Random.value * (zMax - zMin) + zMin;
        return new Boid(this, x, y, z);
    }
}
