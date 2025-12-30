package dsa;

import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.regex.*;
import java.util.stream.*;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;

public class prob_trie {

//class Result {

    public class TrieNode {
        char val;
        boolean isLeaf;
        Map<Character,TrieNode>  children = new HashMap<>();
        TrieNode(char val) {
            this.val = val;
        }
        TrieNode getNext(char c) {
           TrieNode reply = null;
           //System.out.println(".getNext("+c+") ");
           if(children.containsKey(c))
               reply=children.get(c);
           return reply;
        }
        void addNext(TrieNode next) {
            //System.out.println("("+this.val+").addNext("+next.val+") ");
            if(next!=null)
                children.put(next.val,next);
        }
        boolean isLeaf() { return isLeaf; }

        public List<TrieNode> getChildren() {
            return new ArrayList<>(children.values());
        }

        @Override
        public String toString() {
            return "[("+super.toString()+"), val="+val+",  isLeaf="+isLeaf+", children="+children.size()+"]";
        }
    }
    void add2Trie(TrieNode root, String val) {
        TrieNode current = root;
        for(char c : val.toCharArray()) {
            TrieNode next = current.getNext(c);
            if(next==null) {
                TrieNode n = new prob_trie.TrieNode(c);
                current.addNext(n);
                current = n;
            } else
                current=next;
        }
        current.isLeaf = true;
        //System.out.println("add2Trie("+val+") "+current.toString());
    }
    int countLeafNodes(TrieNode root) {
        int cnt = 0;
        //System.out.println("countLeafNodes("+root+")");

        if(root==null) return 0;
        if(root.isLeaf()) cnt++;
        for(TrieNode c: root.getChildren())
            cnt += countLeafNodes(c);
        return cnt;
    }
    int countPrefixMatch(TrieNode root, String prefix) {
        int reply = 0;
        TrieNode current = root;
        int level;
        char[] prefixArray = prefix.toCharArray();
        int i;
        //System.out.println("countPrefixMatch("+prefix+") "+current.toString());
        for(i=0; current!=null && i<prefixArray.length; i++) {
            //System.out.println("countPrefixMatch("+prefix+") looking for-"+prefixArray[i]);
            TrieNode next = current.getNext(prefixArray[i]);
            if(next!=null) {
                //System.out.println("countPrefixMatch("+prefix+") found-"+prefixArray[i]);
                current = next;
            } else {
                current=null;
                break;
            }
        }
        if(current!=null) {
            reply = countLeafNodes(current);
        }
        return reply;
    }
    /*
     * Complete the 'contacts' function below.
     *
     * The function is expected to return an INTEGER_ARRAY.
     * The function accepts 2D_STRING_ARRAY queries as parameter.
     */
    public List<Integer>
    contacts(List<List<String>> queries) {
        // Write your code here
        TrieNode names = new TrieNode('_');
        List<Integer> response = new ArrayList<>();

        for(List<String> line: queries){
            if(line.get(0).startsWith("add")) {
                add2Trie(names,line.get(1).trim());
            } else if(line.get(0).startsWith("find")){
                String prefix = line.get(1).trim();
                response.add(countPrefixMatch(names,prefix));
            }
        }
        return response;
    }

    public static List<Integer>
    contacts2(List<List<String>> queries) {
        // Write your code here
        List<String> names = new ArrayList<>();
        List<Integer> response = new ArrayList<>();

        for(List<String> line: queries){
            if(line.get(0).startsWith("add")) {
                names.add(line.get(1).trim());
            } else if(line.get(0).startsWith("find")){
                int sum =0;
                String prefix = line.get(1).trim();
                for(String name: names)
                    if(name.startsWith(prefix)) sum++;
                response.add(sum);
            }
        }
        return response;
    }


    public static List<List<String>>
    loadFromFile(String fileName) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new FileReader(fileName));
        //BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        int queriesRows = Integer.parseInt(bufferedReader.readLine().trim());

        List<List<String>> queries = new ArrayList<>();

        IntStream.range(0, queriesRows).forEach(i -> {
            try {
                queries.add(
                        Stream.of(bufferedReader.readLine().replaceAll("\\s+$", "").split(" "))
                                .collect(toList())
                );
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        });
        bufferedReader.close();
        return queries;
    }

    public static void
    main(String[] args) throws IOException {
        List<List<String>> queries = new ArrayList<>();
        String[][] cmds = {{"add", "ed"},
                            {"add","eddie"},
                            {"add","edward"},
                            {"find","ed"},
                            {"add","edwina"},
                            {"find","edw"},
                            {"find","a"}};
        /**
         * add ed
         * add eddie
         * add edward
         * find ed
         * add edwina
         * find edw
         * find a
         */
        int i;
        for(i=0;i<cmds.length;i++)
            queries.add(new ArrayList<String>(Arrays.asList(cmds[i][0],cmds[i][1])) );
        prob_trie solver = new prob_trie();
        List<Integer> result = solver.contacts(queries);
        System.out.println(result.toString());

        queries = loadFromFile("./data/trie_test1_input.txt");
        result = solver.contacts(queries);
        System.out.println(result.toString());

    }

    public static void main2(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        int queriesRows = Integer.parseInt(bufferedReader.readLine().trim());

        List<List<String>> queries = new ArrayList<>();

        IntStream.range(0, queriesRows).forEach(i -> {
            try {
                queries.add(
                        Stream.of(bufferedReader.readLine().replaceAll("\\s+$", "").split(" "))
                                .collect(toList())
                );
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        });
        prob_trie solver = new prob_trie();
        List<Integer> result = solver.contacts(queries);

        bufferedWriter.write(
                result.stream()
                        .map(Object::toString)
                        .collect(joining("\n"))
                        + "\n"
        );

        bufferedReader.close();
        bufferedWriter.close();
    }
}

