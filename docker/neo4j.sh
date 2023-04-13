
docker run \
    -p 7474:7474 -p 7687:7687 \
    -d \
    --rm \
    -e NEO4J_AUTH=neo4j/admintest \
    neo4j:latest


// Genesisブロックの作成
CREATE (b1:Block {name: 'Genesis', date: '2023-01-01'})
//RETURN b1

// 2番目のブロックの作成
CREATE (b2:Block {name: 'Block 2', date: '2023-01-02'})
CREATE (b1)-[:PREVIOUS]->(b2)
//RETURN b2

// 3番目のブロックの作成
CREATE (b3:Block {name: 'Block 3', date: '2023-01-03'})
CREATE (b2)-[:PREVIOUS]->(b3)
//RETURN b3


MATCH p=(b:Block)-[:PREVIOUS*]->(last:Block)
WHERE NOT ()-[:PREVIOUS]->(b)
RETURN nodes(p) as Blocks
