using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Building {
    public int[,] floorPlan;

    public int width;
    public int height;
    public int floorHeight;

    public int maxFloors = 1;
    public int minFloors = 1;

    public Texture2D window;
    public int windowWidth = 2;
    public int windowHeight = 3;
    public int idealWindowNumber = 10;
    public float windowThreshold = 1;

    public Texture2D door;
    public int doorWidth = 2;
    public int doorHeight = 3;
    public int maxDoorNumber = 2;
    public int numDoors = 1;
    
    public int roofType = 1;

    public Color color;

    public float xPos = 0;

    public Building(int[,] fp, int w, int h, int fh) {
        floorPlan = fp;
        width = w;
        height = h;
        floorHeight = fh;
    }

    public void randomize() {
        int floors = (int) Mathf.Round(Random.value * (maxFloors - minFloors) + minFloors);
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                floorPlan[x, y] *= floors;
            }
        }
        
        Texture2D[] windows = 
            {(Texture2D) Resources.Load("window1"), 
             (Texture2D) Resources.Load("window2"), 
             (Texture2D) Resources.Load("window3")};
        int[] windowWidths =
            {2, 2, 2};
        int[] windowHeights =
            {3, 2, 3};
        int windowRand = (int) Mathf.Round(Random.value * 2);
        window = windows[windowRand];
        windowWidth = windowWidths[windowRand];
        windowHeight = windowWidths[windowRand];
        windowThreshold = Random.value;

        Texture2D[] doors =
            {(Texture2D) Resources.Load("door1"),(Texture2D) Resources.Load("door2"),(Texture2D) Resources.Load("door3")};
        int[] doorWidths =
            {2, 3, 3};
        int[] doorHeights =
            {3, 3, 3};
        int doorRandom = (int) Mathf.Round(Random.value * 2);
        door = doors[doorRandom];
        doorWidth = doorWidths[doorRandom];
        doorHeight = doorHeights[doorRandom];
        numDoors = (int) Mathf.Round(Random.value * maxDoorNumber) + 2;

        int[] roofTypes =
            {0, 1};
        int roofRandom = (int) Mathf.Round(Random.value);
        roofType = roofTypes[roofRandom];

        Color[] colors =
            {new Color(0.0f, 0.2f, 1.0f, 1.0f), new Color(0.6f, 0.0f, 0.0f, 1.0f), new Color(1.0f, 0.95f, 0.5f, 1.0f), new Color (0.1f, 0.1f, 0.1f, 1.0f), new Color(0.1f, 0.8f, 0.3f, 1.0f)};
        int colorRandom = (int) Mathf.Round(Random.value * 4);
        color = colors[colorRandom];
    }

    public static Building getBuilding() {
        int[,] plan1 = {{0, 1, 0},
                        {1, 1, 1},
                        {0, 1, 0}};
        Building cross = new Building(plan1, 3, 3, 5);
        cross.minFloors = 1;
        cross.maxFloors = 3;

        int[,] plan2 = {{1}};
        Building skyScraper = new Building(plan2, 1, 1, 5);
        skyScraper.minFloors = 5;
        skyScraper.maxFloors = 10;

        int[,] plan3 = {{1, 1, 1},
                        {1, 0, 1},
                        {1, 1, 1}};
        Building courtyard = new Building(plan3, 3, 3, 5);
        courtyard.minFloors = 2;
        courtyard.maxFloors = 2;

        int[,] plan4 = {{1, 1, 1},
                        {1, 0, 1},
                        {1, 0, 1}};
        Building estate = new Building(plan4, 3, 3, 5);
        estate.minFloors = 2;
        estate.maxFloors = 3;

        int[,] plan5 = {{4, 4, 4, 4, 0, 0, 4, 4, 4, 4},
                        {4, 5, 5, 4, 3, 3, 4, 5, 5, 4},
                        {4, 5, 5, 4, 3, 3, 4, 5, 5, 4},
                        {4, 4, 4, 4, 0, 0, 4, 4, 4, 4}};
        Building parliament = new Building(plan5, 4, 10, 5);
        
        int[,] plan6 = {{1, 1, 1},
                        {1, 0, 0},
                        {1, 0, 0}};
        Building l = new Building(plan6, 3, 3, 5);
        l.minFloors = 1;
        l.maxFloors = 2;

        int[,] plan7 = {{0, 0, 3, 0, 0},
                        {0, 4, 4, 4, 0},
                        {3, 4, 5, 4, 3},
                        {0, 4, 4, 4, 0},
                        {0, 0, 3, 0, 0}};
        Building longScraper = new Building(plan7, 5, 5, 5);
        longScraper.minFloors = 1;
        longScraper.maxFloors = 2;

        int[,] plan8 = {{3, 1, 3},
                        {1, 0, 1},
                        {3, 1, 3}};
        Building cornerPoints = new Building(plan8, 3, 3, 5);

        int[,] plan9 = {{1, 0, 1, 0, 1},
                        {1, 0, 1, 0, 1},
                        {1, 0, 1, 0, 1},
                        {1, 0, 1, 0, 1},
                        {1, 0, 1, 0, 1}};
        Building barracks = new Building(plan9, 5, 5, 5);
        barracks.maxDoorNumber = 1000;

        int[,] plan10 = {{1, 1, 1},
                         {1, 1, 1}};
        Building duplex = new Building(plan10, 2, 3, 5);
        duplex.minFloors = 2;
        duplex.maxFloors = 2;
        duplex.maxDoorNumber = 1000;

        int[,] plan11 = {{3, 2, 1, 2, 3},
                         {2, 0, 0, 0, 2},
                         {1, 0, 0, 0, 1},
                         {2, 0, 0, 0, 2},
                         {3, 2, 1, 2, 3}};
        Building escher = new Building(plan11, 5, 5, 5);

        int[,] plan12 = {{5, 4, 3},
                         {4, 3, 2},
                         {3, 2, 1}};
        Building gradient = new Building(plan12, 3, 3, 5);

        Building[] buildings = {cross, skyScraper, courtyard, estate, l, longScraper, parliament, cornerPoints, barracks, duplex, escher, gradient};

        int rand = (int)Mathf.Round(Random.value * 11);
        
        Building b = buildings[rand];
        b.randomize();
        return b;
    }
}