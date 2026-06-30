using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RadiusFilter {
    public bool closeStart = false;
    public bool closeEnd = false;
    public bool parabola = false;
    public bool linear = false;

    float radius = 1;

    public float theta = 0;
    public float noiseMultiplier = 0;
    public float noiseRangeMax = 1.0f;

    public float spineEpsilon = 0.0f;
    public float spineSize = 0.0f;
    public int spineNumber = 0;
   

    public RadiusFilter() {
    }

    public RadiusFilter(float rad) {
        radius = rad;
    }

    public float getRadius(float t) {
        if (closeStart && t <= 0) {
            return 0f;
        } else if (closeEnd && t >= 1) {
            return 0f;
        }
        
        float multiplier = 0;

        if (parabola) {
            multiplier = (-1f * (1.8f * t - 1f) * (1.8f * t - 1f) + 1f);
        } else if (linear) {
            multiplier = (1 - t);
        } else {
            multiplier = 1;
        }

        float noise = 0.5f * Mathf.PerlinNoise(t * 2, theta * 2)
                    + 0.25f * Mathf.PerlinNoise(t * 4, theta * 4)
                    + 0.1f * Mathf.PerlinNoise(t * 10, theta * 10);

        noise *= noiseMultiplier;

        if (t > noiseRangeMax) {
            noise = 0;
        }

        if (theta > -1 * spineEpsilon && theta < spineEpsilon) {
            multiplier += spineSize * Mathf.Abs(Mathf.Sin(t * Mathf.PI * spineNumber));
        }

        return (radius + noise) * multiplier;

        //float x = p.x;
        //float y = p.y + Mathf.Cos(theta) * r;
        //float z = zPos + Mathf.Sin(theta) * r;

        //float r = (radius * radius) * l / linGran;

         //+ 
                  //(0.5f * Mathf.PerlinNoise(phi * 2, theta * 2)
                  //+ 0.25f * Mathf.PerlinNoise(phi * 4, theta * 4)
                  //+ 0.1f * Mathf.PerlinNoise(phi * 10, theta * 10));
    }

    public void closeEnds() {
        closeStart = true;
        closeEnd = true;
    }
}