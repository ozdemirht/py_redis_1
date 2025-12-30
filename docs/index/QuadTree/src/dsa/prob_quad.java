package dsa;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class prob_quad {
    public class Point {
        private float x, y;
    }
    public class Region {
        private Point min;
        private Point max;
    }
    public class PointRecord<T> {
        Point location;
        private T value;
    }
    public class QuadTreeNode {
        private Region area; // rectangular boundary definition
        // Capacity 1, or more
        private List<PointRecord> points = new ArrayList<>();
        // 4 children
        private List<QuadTreeNode> children = new ArrayList<>();

        public void insert(PointRecord p){
        }

        public List<PointRecord> queryRange(Point center, float radius){
            return null;
        }
    }

    public class QuadTree {
        private QuadTreeNode root;

        public void insert(PointRecord p){
            root.insert(p);
        }

        public List<PointRecord> queryRange(Point center, float radius){
            return root.queryRange(center, radius);
        }
    }

    public static void
    main(String[] args) throws IOException {
        QuadTree myQuadTree = new prob_quad().new QuadTree();

    }
}
