using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//world generation
//Aiming for fantasy style mountains with lakes,
//dense forests, and treacherous peaks.
public class GenerateWorld : MonoBehaviour {

    private Vector3[] verts;
    private float[,] heights;
    private int[] tris;
    private int width = 100;
    private int height = 100;

    //Coordinates that have already been generated
    private ArrayList mountainCoords;

    //Seed for random number generator
    public int seed = 0;

	// Use this for initialization
	void Start () {
        Random.seed = seed;
        mountainCoords = new ArrayList();
        createMountains(0, 0);
	}
	
	// Update is called once per frame
	void Update () {
        float dx = Input.GetAxis("Horizontal");
        float dz = Input.GetAxis("Vertical");

        if (Camera.current != null) {
            Camera.current.transform.Translate(0, 0, 0.3f * dz);
            Camera.current.transform.Rotate(0, dx * 5.0f, 0);
        }

        Vector3 cam_pos = Camera.main.transform.position;
        createMountains(cam_pos.x, cam_pos.z);
        
	}

    //Creates mountains in the nearby grid location
    void createMountains(float x, float z) {
        //The grid location where the unit is one width / height
        int coordX = (int) Mathf.Round((x - 0.5f * width) / width);
        int coordZ = (int) Mathf.Round((z - 0.5f * height) / height);
        string index = coordX + ", " + coordZ;

        //Don't bother regenerating the same piece of land
        if (mountainCoords.Contains(index)) {
            return;
        }

        mountainCoords.Add(index);

        //Generate terrain, textures and mesh
        Texture2D texture = generateTerrainAndTexture(coordX * width, coordZ * height);
		Mesh my_mesh = createMeshFromTerrain();
        
        GameObject s = new GameObject("Terrain" + index);
        s.AddComponent<MeshFilter>();
        s.AddComponent<MeshRenderer>();
        s.transform.position = new Vector3(coordX * width, 0, coordZ * height);

        s.GetComponent<MeshFilter>().mesh = my_mesh;

        Renderer renderer = s.GetComponent<Renderer>();
        renderer.material.mainTexture = texture;
        
        //Comment previous line out, make the world matte
        //Material material = new Material(Shader.Find("Diffuse"));
        //material.mainTexture = texture;
        //renderer.material = material;
    }

    //offset the world so that there's no mirroring over the axes, like a second seed
    int offset = 20000;
    //seed for perlin noise
    public int perlinSeed = 0;
    Texture2D generateTerrainAndTexture(int i, int j) {
        //Important variables for world generation
        heights = new float[width + 1, height + 1];
        Texture2D texture = new Texture2D(width + 1, height + 1);
        Color[] colors = new Color[(width + 1) * (height + 1)];

        //Volcano variables
        float maxHeight = 0;
        Vector2 maxLocation = new Vector2(0, 0);

        //Lake variables
        float minHeight = 10000;
        Vector2 minLocation = new Vector2(0, 0);
        
        //Iteratively generate vertices
        for (int x = 0; x <= width; x++) {
            for (int z = 0; z <= height; z++) {
                //Swap this line in for a malleable world (change variables by perlinWithBands)
                //heights[x, z] = perlinWithBands(1.0f * x / width, 1.0f * z / height, 5);

                //Three band perlin noise
                float perlinValue = 20.0f * Mathf.PerlinNoise(1.0f * (x + i + offset) / width, 1.0f * (z + j + offset) / height)
                              + 12.0f * Mathf.PerlinNoise(8.0f * (x + i + offset) / width, 3.0f * (z + j + offset) / height)
                              + 5.0f * Mathf.PerlinNoise(16.0f * (x + i + offset) / width, 9.0f * (z + j + offset) / height);

                heights[x, z] = perlinValue;

                //Process volcano/lake variables
                if (perlinValue > maxHeight) {
                    maxHeight = perlinValue;
                    maxLocation = new Vector2(x, z);
                }
                if (perlinValue < minHeight) {
                    minHeight = perlinValue;
                    minLocation = new Vector2(x, z);
                }

                //texture mapping
                int index = z + x * (height + 1);
                float factor = 0.6f * (heights[x, z] / 22);
                Color color = new Color(0.2f, 0.8f - factor, 0.2f, 1.0f);
                if (heights[x, z] > 22) {
                    color = new Color(1.0f, 1.0f, 1.0f, 1.0f);
                }
                colors[index] = color;
            }
        }

        //Locations that we can't grow trees at
        ArrayList bannedLocations = new ArrayList();
        
        //Generate volcano at tallest peak on the newly generated map
        Area volcano = locationsInThreshold(maxLocation, 1.0f);
        ArrayList volcanoLocations = volcano.getArea();
        ArrayList volcanoRim = volcano.getEdge();
        foreach (var loc in volcanoLocations) {
            Vector2 location = (Vector2) loc;
            int x = (int) location.x;
            int z = (int) location.y;
            heights[x, z] = maxHeight - 4.0f;

            int index = z + x * (height + 1);
            colors[index] = new Color(0.8f, 0.2f, 0.2f);

            bannedLocations.Add(location);
        }
        //fix coloration at rim
        foreach (var loc in volcanoRim) {
            Vector2 location = (Vector2) loc;
            int x = (int) location.x;
            int z = (int) location.y;

            int index = z + x * (height + 1);
            colors[index] = new Color(0.2f, 0.2f, 0.2f);
        }

        //Generate lake at lowest valley on the newly generated map
        Area lake = locationsInThreshold(minLocation, 3.5f);
        ArrayList lakeLocations = lake.getArea();
        ArrayList lakeFront = lake.getEdge();
        foreach (var loc in lakeLocations) {
            Vector2 location = (Vector2) loc;
            int x = (int) location.x;
            int z = (int) location.y;
            heights[x, z] = minHeight + 3.5f;

            int index = z + x * (height + 1);
            colors[index] = new Color(0.2f, 0.2f, 0.9f);

            bannedLocations.Add(location);
        }
        //Generate trees around the lake
        ArrayList trees = spread(lakeFront, bannedLocations, 0.6f * Random.value);
        foreach (var loc in trees) {
            Vector2 location = (Vector2) loc;
            int x = (int) location.x;
            int z = (int) location.y;
            float y = heights[x, z];
            placeTree(i + x, y, j + z);
        }

        //Generate some more forests
        for (int n = 0; n < 20; n++) {
            float offsetX = Random.value * width;
            float offsetZ = Random.value * height;
            ArrayList treeSeed = new ArrayList();
            treeSeed.Add(new Vector2(offsetX, offsetZ));
            ArrayList forest = spread(treeSeed, bannedLocations, 0.2f + 0.3f * Random.value);
            foreach (var loc in forest) {
                Vector2 location = (Vector2) loc;
                int x = (int) location.x;
                int z = (int) location.y;
                float y = heights[x, z];
                placeTree(i + x, y, j + z);
            }
        }

        //Build and return texture
        texture.SetPixels(colors);
        texture.Apply();
        return texture;
    }

    //Build mesh, tris and UV for the newly generated map
    Mesh createMeshFromTerrain() {
        Mesh mesh = new Mesh();
        
        int num_verts = (width + 1) * (height + 1);
        verts = new Vector3[num_verts];

        Vector2[] uv = new Vector2[num_verts];

        for (int x = 0; x <= width; x++) {
            for (int z = 0; z <= height; z++) {
                int index = z + x * (height + 1);
                verts[index] = new Vector3(x, heights[x, z], z);
                uv[index] = new Vector2(1.0f * z / height, 1.0f *  x / width);
            }
        }

        int num_tris = width * height * 2;
        tris = new int[num_tris * 3];

        for (int x = 0; x < width; x++) {
            for (int z = 0; z < height; z++) {
                int tris_index = z + x * height;
                int index = z + x * (height + 1);
                tris[tris_index * 6]     = index;
                tris[tris_index * 6 + 1] = index + 1;
                tris[tris_index * 6 + 2] = z + (x + 1) * (height + 1);
                tris[tris_index * 6 + 3] = index + 1;
                tris[tris_index * 6 + 4] = (z + 1) + (x + 1) * (height + 1);
                tris[tris_index * 6 + 5] = z + (x + 1) * (height + 1);
            }
        }

        mesh.vertices = verts;
        mesh.triangles = tris;
        mesh.uv = uv;

        mesh.RecalculateNormals();

        return mesh;
    }

    // UTILITY FUNCTIONS \\

    public float ampScale = 10.0f; //Amplitude
    public float freqScale = 1.0f; //Frequency
    public float bandScale = 2.0f; //Factor scaled between bands

    //Auto generate multi-band perlin noise based on a location and variables
    float perlinWithBands(float x, float z, int bands) {
        float total = 0.0f;
        float currScale = ampScale;
        float internalScale = freqScale;
        
        for (int i = 0; i < bands; i++) {
            total += ampScale * Mathf.PerlinNoise(internalScale * x, internalScale * z);
            currScale /= bandScale;
            internalScale *= bandScale;
        }

        return total;
    }

    //Put tree at the specified 3d coordinate (relative to world)
    void placeTree(float x, float y, float z) {
        GameObject trunk = GameObject.CreatePrimitive(PrimitiveType.Cube);
        trunk.transform.position = new Vector3(x, y, z);
        trunk.transform.localScale = new Vector3(0.3f, 2f, 0.3f);
        
        Renderer renderer = trunk.GetComponent<Renderer>();
        renderer.material.color = new Color(0f, 0f, 0f, 1.0f);

        GameObject leaves = GameObject.CreatePrimitive(PrimitiveType.Cube);
        leaves.transform.position = new Vector3(x, y + 1.5f, z);
        leaves.transform.localScale = new Vector3(1f, 1f, 1f);
        
        float factor = 0.5f * (y / 22) * Random.value;
        Color color = new Color(0.3f, 0.9f - factor, 0.3f, 1.0f);
        Renderer renderer2 = leaves.GetComponent<Renderer>();
        renderer2.material.color = color;//new Color(0.2f, 0.8f, 0.2f, 1.0f);
    }

    //Spread trees
    ArrayList spread(ArrayList start, ArrayList blocked, float spread) {
        //Final locations
        ArrayList locations = new ArrayList();
        //Locations that have been expanded already
        ArrayList expanded = blocked;
        Stack<Vector2> open = new Stack<Vector2>();

        //Add the start to the open list
        foreach (var loc in start) {
            open.Push((Vector2) loc);
        }

        while (open.Count > 0) {
            Vector2 curr = open.Pop();
            int x = (int) curr.x;
            int z = (int) curr.y;
            if (!expanded.Contains(curr) && x <= width && x >= 0 && z <= height && z >= 0) {
                if (Random.value < spread) {
                    //If we should spread, add to spawned trees and seed adjacent locations
                    locations.Add(curr);
                    open.Push(new Vector2(x - 1, z));
                    open.Push(new Vector2(x + 1, z));
                    open.Push(new Vector2(x, z - 1));
                    open.Push(new Vector2(x, z + 1));
                }
                expanded.Add(curr);
            }
        }
        return locations;
    }
    
    //From a central location, find adjacent grid locations that are of similar elevation
    Area locationsInThreshold(Vector2 p, float diff, bool quitOnEdge = true) {
        ArrayList expanded = new ArrayList();
        ArrayList inThreshold = new ArrayList();
        ArrayList edge = new ArrayList();
        Stack<Vector2> open = new Stack<Vector2>();
        open.Push(p);

        //baseline for comparison
        float baseline = heights[(int) p.x, (int) p.y];
        while (open.Count > 0) {
            Vector2 curr = open.Pop();
            int x = (int) curr.x;
            int z = (int) curr.y;
            if (!expanded.Contains(curr)) {
                if (x <= width && x >= 0 && z <= height && z >= 0) {
                    if (Mathf.Abs(baseline - heights[x, z]) <= diff) {
                        inThreshold.Add(curr);
                        open.Push(new Vector2(x - 1, z));
                        open.Push(new Vector2(x + 1, z));
                        open.Push(new Vector2(x, z - 1));
                        open.Push(new Vector2(x, z + 1));
                    } else {
                        edge.Add(curr);
                    }
                } else if (quitOnEdge) {
                    //If we collide with the edge of the map, abort so we don't have weird polys
                    return new Area(new ArrayList(), new ArrayList());
                }
            }
            expanded.Add(curr);
        }
        //Return the spread and the edge of the area
        return new Area(inThreshold, edge);
    }

    //A wrapper class so we can easily store the area and the edge of the area
    public class Area {
        ArrayList area;
        ArrayList edge;
        
        public Area(ArrayList a, ArrayList e) {
            area = a;
            edge = e;
        }

        public ArrayList getArea() {
            return area;
        }

        public ArrayList getEdge() {
            return edge;
        }
    }
}
