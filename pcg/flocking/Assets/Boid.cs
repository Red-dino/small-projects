using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Boid {
    public GameObject gameObj;
    public Vector3 position;
    public Vector3 velocity;
    public Vector3 acceleration;
    public Vector3 force;
    public float mass;

    private float[] weights;

    private float epsilon = 0.000001f;

    private Color color;

    public Boid(Flock flock): this(flock, 0f, 0f, 0f) {
    }

    public Boid(Flock flock, float x, float y, float z) {
        position = new Vector3(x, y, z);
        velocity = new Vector3(0, 0, 0);
        mass = 5.0f;

        color = new Color(Random.value, Random.value, Random.value, 1.0f);

        gameObj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        gameObj.transform.position = position;
        gameObj.transform.localScale = new Vector3(1f, 0.2f, 0.2f);
        gameObj.GetComponent<Renderer>().material.color = color;

        GameObject pointer = GameObject.CreatePrimitive(PrimitiveType.Cube);
        pointer.transform.position = new Vector3(x + 0.5f, y, z);
        pointer.transform.localScale = new Vector3(0.2f, 0.05f, 0.05f);
        pointer.GetComponent<Renderer>().material.color = Color.red;
        pointer.transform.parent = gameObj.transform;
        
        if (flock.wings) {
            GameObject wings = GameObject.CreatePrimitive(PrimitiveType.Cube);
            wings.transform.position = new Vector3(x, y, z);
            wings.transform.localScale = new Vector3(0.2f, 0.05f, 1.5f);
            wings.GetComponent<Renderer>().material.color = color;
            wings.transform.parent = gameObj.transform;
        }
    }

    public void update(Flock flock, float timeStep) {
        Vector3 wanderingForce = new Vector3(Random.value * 2.0f - 1, Random.value * 2.0f - 1, Random.value * 2.0f - 1);
        Vector3 centeringForce = new Vector3(0f, 0f, 0f);
        Vector3 collisionForce = new Vector3(0f, 0f, 0f);
        Vector3 velocitymForce = new Vector3(0f, 0f, 0f);
        float normalize = 0f;
        for (int i = 0; i < flock.numBoids; i++) {
            Boid boid = flock.boids[i];
            float distance = Vector3.Distance(position, boid.position);
            float weight = 1f / (Mathf.Pow(distance, 2) + epsilon);
            
            if (this != boid) {
                if (distance < flock.centeringRadius) {
                    centeringForce += mult(flock.boids[i].position - position, weight);
                    normalize += weight;
                }
                if (distance < flock.collisionRadius) {
                    collisionForce += mult(position - flock.boids[i].position, weight);
                }
                if (distance < flock.velocitymRadius) {
                    velocitymForce += mult(flock.boids[i].velocity - velocity, weight);
                }
            }
        }
        if (normalize != 0) {
            centeringForce = mult(centeringForce, 1.0f / normalize);
        } else {
            centeringForce = new Vector3(0f, 0f, 0f);
        }
        //velocity matching
        //collision avoidance

        force = mult(wanderingForce, flock.wanderingWeight)
              + mult(centeringForce, flock.centeringWeight)
              + mult(collisionForce, flock.collisionWeight)
              + mult(velocitymForce, flock.velocitymWeight);
        acceleration = mult(force, 1.0f / mass);
        velocity = velocity + mult(acceleration, timeStep);
        float speed = velocity.magnitude; 
        if (speed > flock.maxVel) {
            velocity = mult(velocity.normalized, flock.maxVel);
        } else if (speed < flock.minVel) {
            if (speed == 0) {
                velocity = Vector3.right;
            }
            velocity = mult(velocity.normalized, flock.minVel);
        }
        position = position + mult(velocity, timeStep);

        gameObj.transform.rotation = Quaternion.Euler(calcOrientation(velocity));

        if (position.x < flock.xMin || position.x > flock.xMax) {
            velocity.x *= -1f;
        }
        if (position.y < flock.yMin || position.y > flock.yMax) {
            velocity.y *= -1f;
        }
        if (position.z < flock.zMin || position.z > flock.zMax) {
            velocity.z *= -1f;
        }

        gameObj.transform.position = position;

        if (flock.trailOn) {
            GameObject trail = GameObject.CreatePrimitive(PrimitiveType.Cube);
            trail.transform.position = position;
            trail.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
            trail.GetComponent<Renderer>().material.color = color;
            UnityEngine.Object.Destroy(trail, flock.trailTime);
        }
    }

    public Vector3 calcOrientation(Vector3 v) {
        Vector3 vPlane = Vector3.ProjectOnPlane(v, Vector3.up);
        float thetaY = Vector3.Angle(Vector3.right, vPlane);
        if (v.z > 0) {
            thetaY *= -1f;
        }

        float thetaZ = Vector3.Angle(v, vPlane);
        if (v.y < 0) {
            thetaZ *= -1f;
        }
        
        return new Vector3(0, thetaY, thetaZ);
    }

    public static Vector3 mult(Vector3 vect, float scalar) {
        return new Vector3(vect.x * scalar, vect.y * scalar, vect.z * scalar);
    }

    public void unitTest() {
        Vector3 v = new Vector3(0f, 0f, 0f);

        v = new Vector3(1f, 1f, 1f);
        Debug.Log(v);
        Debug.Log(calcOrientation(v));
        v = new Vector3(-1f, 1f,  1f);
        Debug.Log(v);
        Debug.Log(calcOrientation(v));
        v = new Vector3(1f, -1f, 1.0f);
        Debug.Log(v);
        Debug.Log(calcOrientation(v));
        v = new Vector3(1f, 1f, -1.0f);
        Debug.Log(v);
        Debug.Log(calcOrientation(v));
        v = new Vector3(-1f, -1f, 1f);
        Debug.Log(v);
        Debug.Log(calcOrientation(v));
        v = new Vector3(-1f, 1f, -1f);
        Debug.Log(v);
        Debug.Log(calcOrientation(v));
        v = new Vector3(1f, -1f, -1f);
        Debug.Log(v);
        Debug.Log(calcOrientation(v));
        v = new Vector3(-1f, -1f, -1f);
        Debug.Log(v);
        Debug.Log(calcOrientation(v));
    }
}
