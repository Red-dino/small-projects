using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bezier : MonoBehaviour {

    public int seed = 1;

	// Use this for initialization
	void Start () {
        Random.seed = seed;

        Vector2 p1 = new Vector2(0, 0);
        Vector2 p2 = new Vector2(2, 4);
        Vector2 p3 = new Vector2(6, 2);
        Vector2 p4 = new Vector2(6, 8);
        BezierCurve b = new BezierCurve(p1, p2, p3, p4);

        //RadiusFilter filter = new RadiusFilter();
        //Mesh mesh = bezierTubeMesh(b, filter, 100, 20);

        for (int i = 0; i < 5; i++) {
            GameObject creature = generateCreature();
            creature.transform.position = new Vector3(0, creature.transform.position.y, 10 * i);
        }
	}
	
	// Update is called once per frame
	void Update () {
	}

    public GameObject generateCreature() {
        float x = 0;
        float y = 0.5f;
        Vector2 p1 = new Vector2(x, y);
        x += Random.value * 3;
        y += Random.value * 3 - 2;
        Vector2 p2 = new Vector2(x, y);
        x += Random.value * 3 + 2;
        y += Random.value * 4 - 2;
        Vector2 p3 = new Vector2(x, y);
        x += Random.value;
        y += Random.value * 3 + 2;
        Vector2 p4 = new Vector2(x, y);
        BezierCurve b = new BezierCurve(p1, p2, p3, p4);

        RadiusFilter filter = new RadiusFilter();
        filter.parabola = true;
        filter.noiseMultiplier = Random.value + 0.2f;
        filter.noiseRangeMax = 0.95f;
        if (Random.value > 0.7) {
            filter.spineEpsilon = Random.value * 0.2f;
            filter.spineNumber = (int) Mathf.Round(Random.value * 20);
            filter.spineSize = Random.value * 1.5f;
        }

        Mesh mesh = bezierTubeMesh(b, filter, 100, 20);

        Color color = new Color(Random.value, Random.value, Random.value, 1.0f);

        GameObject s = new GameObject("creature");
        s.AddComponent<MeshFilter>();
        s.AddComponent<MeshRenderer>();

        s.GetComponent<MeshFilter>().mesh = mesh;
        s.GetComponent<Renderer>().material.color = color;
        
        float floor = minY - (Random.value * 2f) - 1f;

        int legStyle = (int) Mathf.Floor(Random.value * 3 + 1);
        GameObject legs = generateLegs(b, filter, floor, legStyle, color);
        legs.transform.parent = s.transform;

        Vector2 headLoc = b.getCurvePoint(1f);
        Vector3 headOrigin = new Vector3(headLoc.x, headLoc.y, 0);

        int mouthStyle = (int) Mathf.Round(Random.value * 2 + 1);
        GameObject head = generateHumanHead(headOrigin, mouthStyle, color);
        head.transform.parent = s.transform;

        float xScale = 1 + Random.value * 1f;
        float yScale = 1 + Random.value * 0.5f;
        float zScale = 1 + Random.value * 1f;
        head.transform.localScale = new Vector3(xScale, yScale, zScale);

        s.transform.position = new Vector3(0, -floor, 0);
        return s;
    }

    GameObject generateLegs(BezierCurve b, RadiusFilter filter, float floor, int legType, Color color) {
        GameObject legGroup = new GameObject("legGroup");

        float[] legFactor = {5f, 1.8f, 3f, 6f};

        int count = 0;

        float lastX = -100f;
        float maxRad = -1;
        for (int i = 1; i <= 7; i++) {
            if (Random.value > 0.5) {
                float legT = 0.1f * i + 0.1f;
                Vector2 legLoc = b.getCurvePoint(legT);
                float legRad = (Random.value * 0.4f + 0.8f) * filter.getRadius(legT) / legFactor[legType - 1];
                if (maxRad == -1) {
                    maxRad = legRad;
                }
                legRad = Mathf.Min(maxRad, legRad);
                if (legLoc.x > lastX + legRad) {
                    lastX = legLoc.x + legRad;
                    Vector3 origin = new Vector3(legLoc.x, legLoc.y, 0);
                    GameObject leg1 = null;
                    GameObject leg2 = null;
                    if (legType == 1) {
                        leg1 = generateSpiderLeg(origin, legRad, floor);
                        leg2 = generateSpiderLeg(origin, legRad, floor, false);
                    } else if (legType == 2) {
                        leg1 = generateStockyLeg(origin, legRad, floor);
                        leg2 = generateStockyLeg(origin, legRad, floor, false);
                    } else if (legType == 3) {
                        leg1 = generateHumanLeg(origin, legRad, floor);
                        leg2 = generateHumanLeg(origin, legRad, floor, false);
                    } else if (legType == 4) {
                        leg1 = generateChickenLeg(origin, legRad, floor);
                        leg2 = generateChickenLeg(origin, legRad, floor, false);
                    }
                    leg1.transform.parent = legGroup.transform;
                    leg2.transform.parent = legGroup.transform;
                    leg1.GetComponent<Renderer>().material.color = color;
                    leg2.GetComponent<Renderer>().material.color = color;
                    count++;
                }
            }
        }

        if (count == 0) {
            return generateLegs(b, filter, floor, legType, color);
        }
        return legGroup;
    }

    public GameObject generateHumanHead(Vector3 origin, int mouthStyle, Color color) {
        GameObject head = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        head.transform.position = origin;
        head.GetComponent<Renderer>().material.color = color;

        GameObject eye1 = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        eye1.transform.position = new Vector3(origin.x + 0.35f, origin.y + 0.5f, origin.z - 0.3f);
        eye1.transform.localScale = new Vector3(0.2f, 0.2f, 0.2f);
        eye1.transform.parent = head.transform;

        GameObject pupil1 = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        pupil1.transform.position = new Vector3(origin.x + 0.41f, origin.y + 0.5f, origin.z - 0.3f);
        pupil1.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        pupil1.GetComponent<Renderer>().material.color = Color.black;
        pupil1.transform.parent = head.transform;

        GameObject eye2 = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        eye2.transform.position = new Vector3(origin.x + 0.35f, origin.y + 0.5f, origin.z + 0.3f);
        eye2.transform.localScale = new Vector3(0.2f, 0.2f, 0.2f);
        eye2.transform.parent = head.transform;

        GameObject pupil2 = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        pupil2.transform.position = new Vector3(origin.x + 0.41f, origin.y + 0.5f, origin.z + 0.3f);
        pupil2.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        pupil2.GetComponent<Renderer>().material.color = Color.black;
        pupil2.transform.parent = head.transform;

        Vector3 mouthOrigin = new Vector3(origin.x + 0.5f, origin.y - 0.2f, origin.z);
        Vector3 mouthCenter = new Vector3(origin.x, origin.y - 0.2f, origin.z);
        GameObject mouth = null;
        if (mouthStyle == 1) {
            mouth = generateMouth(mouthOrigin);
        } else if (mouthStyle == 2) {
            mouth = generateBeak(mouthOrigin, mouthCenter, 0.5f);
        } else if (mouthStyle == 3) {
            mouth = generateFeelers(mouthOrigin, mouthCenter, color);
        }
        mouth.transform.parent = head.transform;

        return head;
    }

    public GameObject generateMouth(Vector3 origin) {
        GameObject mouth = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        mouth.transform.position = new Vector3(origin.x, origin.y + 0.5f, origin.z);
        mouth.transform.localScale = new Vector3(0.2f, 0.15f, 0.4f);
        mouth.transform.rotation = Quaternion.Euler(90, 0, 0);

        GameObject nose = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        nose.transform.position = origin;
        nose.transform.localScale = new Vector3(0.1f, 0.2f, 0.1f);
        nose.transform.rotation = Quaternion.Euler(90, 0, 0);
        nose.transform.parent = mouth.transform;

        return mouth;
    }

    public GameObject generateFeelers(Vector3 origin, Vector3 center, Color color) {
        RadiusFilter filter = new RadiusFilter(0.05f);
        filter.closeEnds();

        GameObject feelerGroup = new GameObject("feelers");

        for (int i = 0; i < 4; i++) { 
            float z = i / 6.0f - 0.25f;

            Vector2 p1 = new Vector2(center.x, center.y + 0.05f);
            Vector2 p2 = new Vector2(origin.x, origin.y + 0.05f);
            Vector2 p3 = new Vector2(origin.x + 0.1f, origin.y + 0.05f);
            Vector2 p4 = new Vector2(origin.x + 0.2f , origin.y - (0.15f * Random.value));
            BezierCurve b = new BezierCurve(p1, p2, p3, p4);

            Mesh feelerMesh = bezierTubeMesh(b, filter, 20, 10);

            GameObject feeler = new GameObject("feeler" + i);
            feeler.AddComponent<MeshFilter>();
            feeler.AddComponent<MeshRenderer>();

            feeler.GetComponent<MeshFilter>().mesh = feelerMesh;
            feeler.GetComponent<Renderer>().material.color = new Color(0.8f, 0.2f, 0.2f, 1.0f);
            feeler.transform.Translate(0, 0, z);
            feeler.transform.parent = feelerGroup.transform;
            feeler.GetComponent<Renderer>().material.color = color;

            p1 = new Vector2(center.x, center.y - 0.3f);
            p2 = new Vector2(origin.x, origin.y - 0.3f);
            p3 = new Vector2(origin.x + 0.1f, origin.y - 0.3f);
            p4 = new Vector2(origin.x + 0.2f , origin.y - 0.3f + (0.15f * Random.value + 0.05f));
            BezierCurve b2 = new BezierCurve(p1, p2, p3, p4);

            Mesh feelerMesh2 = bezierTubeMesh(b2, filter, 20, 10);

            GameObject feeler2 = new GameObject("lowerFeeler" + i);
            feeler2.AddComponent<MeshFilter>();
            feeler2.AddComponent<MeshRenderer>();

            feeler2.GetComponent<MeshFilter>().mesh = feelerMesh2;
            feeler2.GetComponent<Renderer>().material.color = new Color(0.8f, 0.2f, 0.2f, 1.0f);
            feeler2.transform.Translate(0, 0, z);
            feeler2.transform.parent = feelerGroup.transform;
            feeler2.GetComponent<Renderer>().material.color = color;

        }

        return feelerGroup;
    }

    public GameObject generateBeak(Vector3 origin, Vector3 center, float radius) {
        RadiusFilter filter = new RadiusFilter(radius);
        filter.linear = true;

        Vector2 p1 = new Vector2(center.x, center.y);
        Vector2 p2 = new Vector2(origin.x, origin.y);
        Vector2 p3 = new Vector2(origin.x + 0.25f, origin.y);
        Vector2 p4 = new Vector2(origin.x + 0.5f, origin.y);
        BezierCurve b = new BezierCurve(p1, p2, p3, p4);

        Mesh beakMesh = bezierTubeMesh(b, filter, 20, 4);

        GameObject beak = new GameObject("beak");
        beak.AddComponent<MeshFilter>();
        beak.AddComponent<MeshRenderer>();

        beak.GetComponent<MeshFilter>().mesh = beakMesh;
        beak.GetComponent<Renderer>().material.color = new Color(0.8f, 0.2f, 0.2f, 1.0f);

        return beak;
    }
 
    public GameObject generateSpiderLeg(Vector3 origin, float radius, float floor, bool right = true) {
        RadiusFilter filter = new RadiusFilter(radius);
        filter.parabola = true;
        filter.closeEnds();
        float factor = right ? 1f : -1f;

        Vector2 legP1 = new Vector2(origin.z, origin.y);
        Vector2 legP2 = new Vector2(origin.z + factor * 1, origin.y + 2);
        Vector2 legP3 = new Vector2(origin.z + factor * 3, origin.y + 1);
        Vector2 legP4 = new Vector2(origin.z + factor * 4, floor);
        BezierCurve legB = new BezierCurve(legP1, legP2, legP3, legP4);

        Mesh legMesh = bezierTubeMesh(legB, filter, 4, 20, true);

        GameObject legs = new GameObject("leg");
        legs.AddComponent<MeshFilter>();
        legs.AddComponent<MeshRenderer>();

        legs.GetComponent<MeshFilter>().mesh = legMesh;
        legs.GetComponent<Renderer>().material.color = new Color(0.8f, 0.2f, 0.2f, 1.0f);
        
        legs.transform.Translate(origin.x ,0, 0);
        return legs;
    }

    public GameObject generateStockyLeg(Vector3 origin, float radius, float floor, bool right = true) {
        RadiusFilter filter = new RadiusFilter(radius);
        filter.closeEnds();
        float factor = right ? 1f : -1f;

        Vector2 legP1 = new Vector2(origin.z, origin.y);
        Vector2 legP2 = new Vector2(origin.z + 1 * factor, origin.y);
        Vector2 legP3 = new Vector2(origin.z + 1 * factor, origin.y - 1);
        Vector2 legP4 = new Vector2(origin.z + 1 * factor, floor);
        BezierCurve legB = new BezierCurve(legP1, legP2, legP3, legP4);

        Mesh legMesh = bezierTubeMesh(legB, filter, 100, 20, true);

        GameObject legs = new GameObject("leg");
        legs.AddComponent<MeshFilter>();
        legs.AddComponent<MeshRenderer>();

        legs.GetComponent<MeshFilter>().mesh = legMesh;
        legs.GetComponent<Renderer>().material.color = new Color(0.8f, 0.2f, 0.2f, 1.0f);
        
        legs.transform.Translate(origin.x ,0, 0);
        return legs;
    }
    
    public GameObject generateHumanLeg(Vector3 origin, float radius, float floor, bool right = true) {
        RadiusFilter filter = new RadiusFilter(radius);
        filter.closeEnds();
        float factor = right ? 1f : -1f;

        Vector2 legP1 = new Vector2(origin.x, origin.y);
        Vector2 legP2 = new Vector2(origin.x + 2, origin.y - 1);
        Vector2 legP3 = new Vector2(origin.x + 1, floor + 0.5f);
        Vector2 legP4 = new Vector2(origin.x + 1, floor);
        BezierCurve legB = new BezierCurve(legP1, legP2, legP3, legP4);

        Mesh legMesh = bezierTubeMesh(legB, filter, 100, 20);

        GameObject legs = new GameObject("leg");
        legs.AddComponent<MeshFilter>();
        legs.AddComponent<MeshRenderer>();

        legs.GetComponent<MeshFilter>().mesh = legMesh;
        legs.GetComponent<Renderer>().material.color = new Color(0.8f, 0.2f, 0.2f, 1.0f);
        
        legs.transform.Translate(0 ,0, origin.z + factor * radius * 1.5f);
        return legs;
    }

    public GameObject generateChickenLeg(Vector3 origin, float radius, float floor, bool right = true) {
        RadiusFilter filter = new RadiusFilter(radius);
        filter.closeEnds();
        float factor = right ? 1f : -1f;

        Vector2 legP1 = new Vector2(origin.x, origin.y);
        Vector2 legP2 = new Vector2(origin.x - 1, origin.y - 2);
        Vector2 legP3 = new Vector2(origin.x, floor + 0.5f);
        Vector2 legP4 = new Vector2(origin.x, floor);
        BezierCurve legB = new BezierCurve(legP1, legP2, legP3, legP4);

        Mesh legMesh = bezierTubeMesh(legB, filter, 100, 20);

        GameObject legs = new GameObject("leg");
        legs.AddComponent<MeshFilter>();
        legs.AddComponent<MeshRenderer>();

        legs.GetComponent<MeshFilter>().mesh = legMesh;
        legs.GetComponent<Renderer>().material.color = new Color(0.8f, 0.2f, 0.2f, 1.0f);
        
        legs.transform.Translate(0 ,0, origin.z + factor * radius * 3f);
        return legs;
    }

    float minY = 100;
    Mesh bezierTubeMesh(BezierCurve b, RadiusFilter filter, int linGran, int angGran, bool zOriented=false) {
        minY = 0;

        float radius = 0.8f;
        float zPos = 0.0f;

        int numVerts = (linGran + 1) * angGran;
        int numTris = 2 * linGran * angGran;
        Vector3[] verts = new Vector3[numVerts];
        int[] tris = new int[numTris * 3];

        float linStep = 1f / linGran;
        float angStep = 2f * Mathf.PI / angGran;
        for (int l = 0; l <= linGran; l++) {
            float t = l * linStep;
            Vector2 p = b.getCurvePoint(t);
            Vector2 tangent = b.tangent(t);
            for (int a = 0; a < angGran; a++) {
                float theta = a * angStep;
                float phi = (90 + Vector2.SignedAngle(new Vector2(0, 1), tangent)) * Mathf.Deg2Rad;

                filter.theta = theta;
                float r = filter.getRadius(t);

                float x = 0;
                float y = Mathf.Cos(theta) * r;
                float z = Mathf.Sin(theta) * r;
                float xp = p.x + x * Mathf.Cos(phi) - y * Mathf.Sin(phi);
                float yp = p.y + x * Mathf.Sin(phi) + y * Mathf.Cos(phi);
                float zp = zPos + z;

                minY = Mathf.Min(minY, yp);

                int i = l * angGran + a;
                if (!zOriented) {
                    verts[i] = new Vector3(xp, yp, zp);
                } else {
                    verts[i] = new Vector3(zp, yp, xp);
                }
            }
        }

        for (int l = 0; l < linGran; l++) {
            for (int a = 0; a < angGran; a++) {
                int i = 6 * (l * angGran + a);
                if (!zOriented) {
                    tris[i + 2] = l * angGran + a;
                    tris[i + 1] = (l + 1) * angGran + ((a + 1) % angGran);
                    tris[i + 0] = l * angGran + ((a + 1) % angGran);
                    tris[i + 5] = l * angGran + a;
                    tris[i + 4] = (l + 1) * angGran + a; 
                    tris[i + 3] = (l + 1) * angGran + ((a + 1) % angGran);
                } else {
                    tris[i + 0] = l * angGran + a;
                    tris[i + 1] = (l + 1) * angGran + ((a + 1) % angGran);
                    tris[i + 2] = l * angGran + ((a + 1) % angGran);
                    tris[i + 3] = l * angGran + a;
                    tris[i + 4] = (l + 1) * angGran + a; 
                    tris[i + 5] = (l + 1) * angGran + ((a + 1) % angGran);
                }
            }
        }

        Mesh mesh = new Mesh();
        mesh.vertices = verts;
        mesh.triangles = tris;

        mesh.RecalculateNormals();

        return mesh;
    }

    class BezierCurve {
        Vector2 p1;
        Vector2 p2;
        Vector2 p3;
        Vector2 p4;

        public BezierCurve(Vector2 p1, Vector2 p2, Vector2 p3, Vector2 p4) {
            this.p1 = p1;
            this.p2 = p2;
            this.p3 = p3;
            this.p4 = p4;
        }

        //t should be on [0, 1]
        public Vector2 getCurvePoint(float t) {
            float i = (1 - t);
            float s1 = i * i * i;
            float s2 = 3 * i * i * t;
            float s3 = 3 * i * t * t;
            float s4 = t * t * t;

            float ansX = s1 * p1.x + s2 * p2.x + s3 * p3.x + s4 * p4.x;
            float ansY = s1 * p1.y + s2 * p2.y + s3 * p3.y + s4 * p4.y;

            return new Vector2(ansX, ansY);
        }

        public Vector2 tangent(float t) {
            Vector2 a = new Vector2(p2.x - p1.x, p2.y - p1.y);
            Vector2 b = new Vector2(p3.x - p2.x, p3.y - p2.y);
            Vector2 c = new Vector2(p4.x - p3.x, p4.y - p3.y);

            float i = (1 - t);
            float s1 = 3 * i * i;
            float s2 = 6 * i * t;
            float s3 = 3 * t * t;

            float ansX = s1 * a.x + s2 * b.x + s3 * c.x;
            float ansY = s1 * a.y + s2 * b.y + s3 * c.y;

            return new Vector2(ansX, ansY);
        }
    }
}
