using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GenerateBuildings : MonoBehaviour {

    public int seed = 22;

	// Use this for initialization
	void Start () {
        Random.seed = seed;

        float xPos = 0;
        for (int i = 0; i < 3; i ++) {
            Building b = Building.getBuilding();
            b.xPos = xPos;
            xPos += b.width * 10 + 10;
            generateWallsFromFloorPlan(b);
        }
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    void generateWallsFromFloorPlan(Building b) {
        int[,] floorPlan = b.floorPlan;
        int width = floorPlan.GetLength(0);
        int length = floorPlan.GetLength(1);
        int numDoors = 0;

        for (int x = 0; x < width; x++) {
            for (int y = 0; y < length; y++) {
                int val = floorPlan[x, y];
                if (val != 0) {
                    if (x == 0 || (x != 0 && floorPlan[x - 1, y] == 0)) {
                        for (int floor = 0; floor < val; floor++) {
                            Vector3 p1 = new Vector3(x * 10 + b.xPos, floor * b.floorHeight, y * 10);
                            Vector3 p2 = new Vector3(x * 10 + b.xPos, floor * b.floorHeight + b.floorHeight, y * 10 + 10);
                            
                            bool genDoor = false;
                            if (floor == 0 && numDoors < b.numDoors && Random.value < 0.5) {
                                genDoor = true;
                                numDoors++;
                            }
                            generateWallWithFeatures(p1, p2, b, true, genDoor);
                        }
                    } else if (x != 0 && floorPlan[x - 1, y] < val) {
                        for (int floor = floorPlan[x - 1, y]; floor < val; floor++) {
                            Vector3 p1 = new Vector3(x * 10 + b.xPos, floor * b.floorHeight, y * 10);
                            Vector3 p2 = new Vector3(x * 10 + b.xPos, floor * b.floorHeight + b.floorHeight, y * 10 + 10);
                            generateWallWithFeatures(p1, p2, b, floor != floorPlan[x - 1, y], floor == 0);
                        }
                    }

                    if (x == width - 1 || (x != width - 1 && floorPlan[x + 1, y] == 0)) {
                        for (int floor = 0; floor < val; floor++) {
                            Vector3 p1 = new Vector3(x * 10 + 10 + b.xPos, floor * b.floorHeight, y * 10 + 10);
                            Vector3 p2 = new Vector3(x * 10 + 10 + b.xPos, floor * b.floorHeight + b.floorHeight, y * 10);
                            
                            bool genDoor = false;
                            if (floor == 0 && numDoors < b.numDoors && Random.value < 0.5) {
                                genDoor = true;
                                numDoors++;
                            }
                            generateWallWithFeatures(p1, p2, b, true, genDoor);
                        }
                    } else if (x != width - 1 && floorPlan[x + 1, y] < val) {
                        for (int floor = floorPlan[x + 1, y]; floor < val; floor++) {
                            Vector3 p1 = new Vector3(x * 10 + 10 + b.xPos, floor * b.floorHeight, y * 10 + 10);
                            Vector3 p2 = new Vector3(x * 10 + 10 + b.xPos, floor * b.floorHeight + b.floorHeight, y * 10);
                            generateWallWithFeatures(p1, p2, b, floor != floorPlan[x + 1, y], floor == 0);
                        }
                    }

                    if (y == 0 || (y != 0 && floorPlan[x, y - 1] == 0)) {
                        for (int floor = 0; floor < val; floor++) {
                            Vector3 p1 = new Vector3(x * 10 + 10 + b.xPos, floor * b.floorHeight, y * 10);
                            Vector3 p2 = new Vector3(x * 10 + b.xPos, floor * b.floorHeight + b.floorHeight, y * 10);
                            //generateWall(p1, p2, "down");
                            
                            bool genDoor = false;
                            if (floor == 0 && numDoors < b.numDoors && Random.value < 0.5) {
                                genDoor = true;
                                numDoors++;
                            }
                            generateWallWithFeatures(p1, p2, b, true, genDoor);
                        }
                    } else if (y != 0 && floorPlan[x, y - 1] < val) {
                        for (int floor = floorPlan[x, y - 1]; floor < val; floor++) {
                            Vector3 p1 = new Vector3(x * 10 + 10 + b.xPos, floor * b.floorHeight, y * 10);
                            Vector3 p2 = new Vector3(x * 10 + b.xPos, floor * b.floorHeight + b.floorHeight, y * 10);
                            generateWallWithFeatures(p1, p2, b, floor != floorPlan[x, y - 1], floor == 0);
                        }
                    }

                    if (y == length - 1 || (y != length - 1 && floorPlan[x, y + 1] == 0)) {
                        for (int floor = 0; floor < val; floor++) {
                            Vector3 p1 = new Vector3(x * 10 + b.xPos, floor * b.floorHeight, y * 10 + 10);
                            Vector3 p2 = new Vector3(x * 10 + 10 + b.xPos, floor * b.floorHeight + b.floorHeight, y * 10 + 10);
                            //generateWall(p1, p2, "right");
                            
                            bool genDoor = false;
                            if (floor == 0 && numDoors < b.numDoors && Random.value < 0.5) {
                                genDoor = true;
                                numDoors++;
                            }
                            generateWallWithFeatures(p1, p2, b, true, genDoor);
                        }
                    } else if (y != length - 1 && floorPlan[x, y + 1] < val) {
                        for (int floor = floorPlan[x, y + 1]; floor < val; floor++) {
                            Vector3 p1 = new Vector3(x * 10 + b.xPos, floor * b.floorHeight, y * 10 + 10);
                            Vector3 p2 = new Vector3(x * 10 + 10 + b.xPos, floor * b.floorHeight + b.floorHeight, y * 10 + 10);
                            generateWallWithFeatures(p1, p2, b, floor != floorPlan[x, y + 1], floor == 0);
                        }
                    }
                    generateRoof(b.roofType, x, y, b, 10);
                }
            }
        }
    }

    void generateRoof(int type, int x, int y, Building b, int unit) {
        int elevation = b.floorPlan[x, y] * b.floorHeight;
        int roofPeak = 3;
        
        if (elevation == 0) { return; }

        if (type == 0) { //Flat roof
            if (elevation != 0) {
                Vector3 p1 = new Vector3(x * unit + b.xPos, elevation, y * unit);
                Vector3 p2 = new Vector3(x * unit + unit + b.xPos, elevation, y * unit);
                Vector3 p3 = new Vector3(x * unit + unit + b.xPos, elevation, y * unit + unit);
                Vector3 p4 = new Vector3(x * unit + b.xPos, elevation, y * unit + unit);
                generateFace(p1, p2, p3, p4, "roof");
            }
        } else if (type == 1) { //Hipped roof
            int[] vertElevations = new int[9];
            int counter = 0;
            for (int i = -1; i <= 1; i++) {
                for (int j = -1; j <= 1; j++) {
                    int indexX = x + i;
                    int indexY = y + j;
                    if (Mathf.Abs(i * j) == 1) {
                        vertElevations[counter] = elevation;
                    } else if (indexX < 0 || indexX >= b.width || indexY < 0 || indexY >= b.height) {
                        vertElevations[counter] = elevation;
                    } else {
                        if (b.floorPlan[indexX, indexY] * b.floorHeight < elevation) {
                            vertElevations[counter] = elevation;
                        } else if (b.floorPlan[indexX, indexY] * b.floorHeight == elevation) {
                            vertElevations[counter] = b.floorPlan[indexX, indexY] * b.floorHeight + roofPeak;
                        } else {
                            vertElevations[counter] = elevation + roofPeak;
                        }
                    }
                    counter++;
                }
            }

            generateRoofFace(vertElevations, x, y, unit, b.xPos);
        }
        Vector3 f1 = new Vector3(x * unit + b.xPos, 0, y * unit);
        Vector3 f2 = new Vector3(x * unit + unit + b.xPos, 0, y * unit);
        Vector3 f3 = new Vector3(x * unit + unit + b.xPos, 0, y * unit + unit);
        Vector3 f4 = new Vector3(x * unit + b.xPos, 0, y * unit + unit);
        generateFace(f4, f3, f2, f1, "floor");
    }

    void generateWallWithFeatures(Vector3 p1, Vector3 p2, Building b, bool windows = true, bool door = true) {
        //List of hitboxes
        List<Rect> features = new List<Rect>();

        bool zOriented = false;
        float width = p2.x - p1.x;
        if (width == 0) {
            zOriented = true;
            width = p2.z - p1.z;
        }
        float wSign = Mathf.Sign(width);

        float height = p2.y - p1.y;
        float hSign = Mathf.Sign(height);

        if (door) {
            int doorWidth = b.doorWidth;
            int doorHeight = b.doorHeight;
            float doorX = Mathf.Abs(width) / 2.0f - doorWidth / 2.0f;  
            Rect doorRect = new Rect(doorX, 0, doorWidth, doorHeight);
            features.Add(doorRect);
            if (zOriented) {
                Vector3 fp1 = new Vector3(p1.x, p1.y + doorRect.yMin, p1.z + wSign * doorRect.xMin);
                Vector3 fp2 = new Vector3(p1.x, p1.y + doorRect.yMax, p1.z + wSign * doorRect.xMax);
                generateWall(fp1, fp2, "door", b.door);
            } else {
                Vector3 fp1 = new Vector3(p1.x + wSign * doorRect.xMin, p1.y + doorRect.yMin, p1.z);
                Vector3 fp2 = new Vector3(p1.x + wSign * doorRect.xMax, p1.y + doorRect.yMax, p1.z);
                generateWall(fp1, fp2, "door", b.door);
            }
        }

        int windowWidth = b.windowWidth;
        int windowHeight = b.windowHeight;
        float windowElevation = 1.0f;
        float threshold = b.windowThreshold;
        int number = b.idealWindowNumber;

        while (threshold + number * (windowWidth + threshold) > Mathf.Abs(width)) {
            number--;
        }
        
        float actualThreshold = (Mathf.Abs(width) - number * windowWidth) / (number + 1.0f);
        float remainingWall = Mathf.Abs(height) - windowElevation - windowHeight;

        if (windows) {
            for (int i = 0; i < number; i++) {
                float windowX = i * (actualThreshold + windowWidth) + actualThreshold;
                Rect windowRect = new Rect(windowX, windowElevation, windowWidth, windowHeight);
                
                bool collision = false;
                foreach (Rect feature in features) {
                    if (windowRect.Overlaps(feature)) {
                        collision = true;
                    }
                }

                if (!collision) {
                    features.Add(windowRect);
                    if (zOriented) {
                        Vector3 fp1 = new Vector3(p1.x, p1.y + windowRect.yMin, p1.z + wSign * windowRect.xMin);
                        Vector3 fp2 = new Vector3(p1.x, p1.y + windowRect.yMax, p1.z + wSign * windowRect.xMax);
                        generateWall(fp1, fp2, "window", b.window);
                    } else {
                        Vector3 fp1 = new Vector3(p1.x + wSign * windowRect.xMin, p1.y + windowRect.yMin, p1.z);
                        Vector3 fp2 = new Vector3(p1.x + wSign * windowRect.xMax, p1.y + windowRect.yMax, p1.z);
                        generateWall(fp1, fp2, "window", b.window);
                    }
                }
            }
        }

        features.Sort((r1, r2)=>r1.xMin.CompareTo(r2.xMin));

        int numFeatures = features.Count;
        int numVerts = 4 * (3 * numFeatures + 1);
        Vector3[] verts = new Vector3[numVerts];

        int numTris = 6 * (3 * numFeatures + 1);
        int[] tris = new int[numTris];

        float currX = 0;
        for (int i = 0; i < numFeatures; i++) {
            Rect feature = features[i];
            float featureWidth = wSign * feature.width;
            float featureHeight = feature.height;
            float gap = wSign * (feature.xMin - currX);
            float off = wSign * currX;
            if (zOriented) {
                //Left part
                verts[i * 12] = new Vector3(p1.x, p1.y, p1.z + off);
                verts[i * 12 + 1] = new Vector3(p1.x, p2.y, p1.z + off);
                verts[i * 12 + 2] = new Vector3(p1.x, p2.y, p1.z + off + gap);
                verts[i * 12 + 3] = new Vector3(p1.x, p1.y, p1.z + off + gap);
                //Below part
                verts[i * 12 + 4] = new Vector3(p1.x, p1.y, p1.z + off + gap);
                verts[i * 12 + 5] = new Vector3(p1.x, p1.y + feature.yMin, p1.z + off + gap);
                verts[i * 12 + 6] = new Vector3(p1.x, p1.y + feature.yMin, p1.z + off + gap + featureWidth);
                verts[i * 12 + 7] = new Vector3(p1.x, p1.y, p1.z + off + gap + featureWidth);
                //Above part
                verts[i * 12 + 8] = new Vector3(p1.x, p1.y + feature.yMax, p1.z + off + gap);
                verts[i * 12 + 9] = new Vector3(p1.x, p2.y, p1.z + off + gap);
                verts[i * 12 + 10] = new Vector3(p1.x, p2.y, p1.z + off + gap + featureWidth);
                verts[i * 12 + 11] = new Vector3(p1.x, p1.y + feature.yMax, p1.z + off + gap + featureWidth);
            } else {
                //Left part
                verts[i * 12] = new Vector3(p1.x + off, p1.y, p1.z);
                verts[i * 12 + 1] = new Vector3(p1.x + off, p2.y, p1.z);
                verts[i * 12 + 2] = new Vector3(p1.x + off + gap, p2.y, p1.z);
                verts[i * 12 + 3] = new Vector3(p1.x + off + gap, p1.y, p1.z);
                //Below part
                verts[i * 12 + 4] = new Vector3(p1.x + off + gap, p1.y, p1.z);
                verts[i * 12 + 5] = new Vector3(p1.x + off + gap, p1.y + feature.yMin, p1.z);
                verts[i * 12 + 6] = new Vector3(p1.x + off + gap + featureWidth, p1.y + feature.yMin, p1.z);
                verts[i * 12 + 7] = new Vector3(p1.x + off + gap + featureWidth, p1.y, p1.z);
                //Above part
                verts[i * 12 + 8] = new Vector3(p1.x + off + gap, p1.y + feature.yMax, p1.z);
                verts[i * 12 + 9] = new Vector3(p1.x + off + gap, p2.y, p1.z);
                verts[i * 12 + 10] = new Vector3(p1.x + off + gap + featureWidth, p2.y, p1.z);
                verts[i * 12 + 11] = new Vector3(p1.x + off + gap + featureWidth, p1.y + feature.yMax, p1.z);
            }
            int trisIndex = i * 18; //0, 2, 1, 0, 3, 2
            //Left part
            tris[trisIndex] = i * 12;
            tris[trisIndex + 1] = i * 12 + 2;
            tris[trisIndex + 2] = i * 12 + 1;
            tris[trisIndex + 3] = i * 12;
            tris[trisIndex + 4] = i * 12 + 3;
            tris[trisIndex + 5] = i * 12 + 2;
            //Bottom part
            tris[trisIndex + 6] = i * 12 + 4;
            tris[trisIndex + 7] = i * 12 + 6;
            tris[trisIndex + 8] = i * 12 + 5;
            tris[trisIndex + 9] = i * 12 + 4;
            tris[trisIndex + 10] = i * 12 + 7;
            tris[trisIndex + 11] = i * 12 + 6;
            //Top part
            tris[trisIndex + 12] = i * 12 + 8;
            tris[trisIndex + 13] = i * 12 + 10;
            tris[trisIndex + 14] = i * 12 + 9;
            tris[trisIndex + 15] = i * 12 + 8;
            tris[trisIndex + 16] = i * 12 + 11;
            tris[trisIndex + 17] = i * 12 + 10;

            currX = feature.xMax;
        }

        if (zOriented) {
            verts[numVerts - 4] = new Vector3(p1.x, p1.y, p1.z + wSign * currX);
            verts[numVerts - 3] = new Vector3(p1.x, p2.y, p1.z + wSign * currX);
            verts[numVerts - 2] = p2;
            verts[numVerts - 1] = new Vector3(p1.x, p1.y, p2.z);
        } else {
            verts[numVerts - 4] = new Vector3(p1.x + wSign * currX, p1.y, p1.z);
            verts[numVerts - 3] = new Vector3(p1.x + wSign * currX, p2.y, p1.z);
            verts[numVerts - 2] = p2;
            verts[numVerts - 1] = new Vector3(p2.x, p1.y, p1.z);
        }
        tris[numTris - 6] = numVerts - 4;
        tris[numTris - 5] = numVerts - 2;
        tris[numTris - 4] = numVerts - 3;
        tris[numTris - 3] = numVerts - 4;
        tris[numTris - 2] = numVerts - 1;
        tris[numTris - 1] = numVerts - 2;

        Mesh mesh = new Mesh();
        mesh.vertices = verts;
        mesh.triangles = tris;
        mesh.RecalculateNormals();
        
        GameObject floor = new GameObject("special");
        floor.AddComponent<MeshFilter>();
        floor.AddComponent<MeshRenderer>();
        floor.GetComponent<MeshFilter>().mesh = mesh;

        Renderer rend = floor.GetComponent<Renderer>();
        rend.material.color = b.color;
    }

    void generateWall(Vector3 p1, Vector3 p2, string name = "Wall", Texture2D tex = null) {
        Vector3 vert1 = p1;
        Vector3 vert2 = new Vector3(p1.x, p2.y, p1.z);
        Vector3 vert3 = p2;
        Vector3 vert4 = new Vector3(p2.x, p1.y, p2.z);
        generateFace(vert1, vert2, vert3, vert4, name, tex);
    }

    void generateFace(Vector3 p1, Vector3 p2, Vector3 p3, Vector3 p4, string name = "Wall", Texture2D tex = null) {
        Mesh floorMesh = new Mesh();
        Vector3[] floorVerts = new Vector3[4];
        floorVerts[0] = p1;
        floorVerts[1] = p2;
        floorVerts[2] = p3;
        floorVerts[3] = p4;
		Vector2[] uv = new Vector2[4];
        uv[0] = new Vector2(1, 0);
		uv[1] = new Vector2(1, 1);
		uv[2] = new Vector2(0, 1);
		uv[3] = new Vector2(0, 0);
        int[] floorTris = new int[6];
        floorTris[0] = 0;
        floorTris[1] = 2;
        floorTris[2] = 1;
        floorTris[3] = 0;
        floorTris[4] = 3;
        floorTris[5] = 2;
        floorMesh.vertices = floorVerts;
        floorMesh.triangles = floorTris;
        floorMesh.uv = uv;
        floorMesh.RecalculateNormals();
        
        GameObject floor = new GameObject(name);
        floor.AddComponent<MeshFilter>();
        floor.AddComponent<MeshRenderer>();
        floor.GetComponent<MeshFilter>().mesh = floorMesh;
        
        Renderer rend = floor.GetComponent<Renderer>();
        if (tex != null) {
            rend.material.mainTexture = tex;
        } else {
            rend.material.color = new Color(0.2f, 0.2f, 0.2f, 1.0f);
        }
    }

    void generateRoofFace(int[] vertElevations, int x, int y, int unit, float xPos) {
        Vector3[] verts = new Vector3[9];
        verts[0] = new Vector3(x * unit + xPos, vertElevations[0], y * unit);
        verts[1] = new Vector3(x * unit + xPos, vertElevations[1], y * unit + (unit / 2.0f));
        verts[2] = new Vector3(x * unit + xPos, vertElevations[2], y * unit + unit);
        verts[3] = new Vector3(x * unit + (unit / 2.0f) + xPos, vertElevations[3], y * unit);
        verts[4] = new Vector3(x * unit + (unit / 2.0f) + xPos, vertElevations[4], y * unit + (unit / 2.0f));
        verts[5] = new Vector3(x * unit + (unit / 2.0f) + xPos, vertElevations[5], y * unit + unit);
        verts[6] = new Vector3(x * unit + unit + xPos, vertElevations[6], y * unit);
        verts[7] = new Vector3(x * unit + unit + xPos, vertElevations[7], y * unit + (unit / 2.0f));
        verts[8] = new Vector3(x * unit + unit + xPos, vertElevations[8], y * unit + unit);
        int[] tris = {4, 3, 0, 1, 4, 0, 2, 4, 1, 5, 4, 2, 4, 6, 3, 7, 6, 4, 8, 7, 4, 8, 4, 5};
        Mesh mesh = new Mesh();
        mesh.vertices = verts;
        mesh.triangles = tris;
        mesh.RecalculateNormals();
        
        GameObject floor = new GameObject("roof");
        floor.AddComponent<MeshFilter>();
        floor.AddComponent<MeshRenderer>();
        floor.GetComponent<MeshFilter>().mesh = mesh;
        
        Renderer rend = floor.GetComponent<Renderer>();
        rend.material.color = new Color(0.2f, 0.2f, 0.2f, 1.0f);
    }
}
