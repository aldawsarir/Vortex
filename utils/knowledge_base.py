"""
Knowledge Base - مستودع المعلومات الجاهزة
مواضيع دراسية جاهزة للطلاب
"""

KNOWLEDGE_BASE = {
    # ============= Computer Science =============
    "python_basics": {
        "title": "Python Programming Basics",
        "category": "💻 Computer Science",
        "icon": "🐍",
        "content": """
Python is a high-level, interpreted programming language known for its simplicity and readability. 
It was created by Guido van Rossum and first released in 1991.

Key Features:
- Easy to learn and read syntax
- Supports multiple programming paradigms (object-oriented, procedural, functional)
- Extensive standard library
- Cross-platform compatibility
- Large community and ecosystem

Basic Syntax:
Variables are declared without type specification. Python uses indentation to define code blocks.
Common data types include integers, floats, strings, lists, tuples, and dictionaries.

Control Structures:
If-else statements control program flow. For and while loops enable iteration.
Functions are defined using the def keyword and can return values.

Object-Oriented Programming:
Python supports classes and objects. Inheritance allows code reuse.
Methods and attributes define object behavior and state.

Popular Applications:
Web development with Django and Flask. Data science with pandas and NumPy.
Machine learning with TensorFlow and scikit-learn. Automation and scripting tasks.
        """
    },
    
    "data_structures": {
        "title": "Data Structures & Algorithms",
        "category": "💻 Computer Science",
        "icon": "🌳",
        "content": """
Data structures organize and store data efficiently for various operations.
Algorithms are step-by-step procedures for solving problems.

Linear Data Structures:
Arrays store elements in contiguous memory locations with constant-time access.
Linked lists use nodes with pointers, allowing dynamic size changes.
Stacks follow Last-In-First-Out (LIFO) principle, used in function calls and undo operations.
Queues follow First-In-First-Out (FIFO) principle, used in task scheduling.

Non-Linear Data Structures:
Trees organize data hierarchically with parent-child relationships.
Binary trees have at most two children per node.
Binary search trees maintain sorted order for efficient searching.
Graphs represent networks of connected nodes and edges.

Hash Tables:
Use hash functions to map keys to array indices.
Provide average constant-time insertion, deletion, and lookup.
Handle collisions using chaining or open addressing.

Algorithm Complexity:
Time complexity measures execution time relative to input size.
Space complexity measures memory usage.
Big O notation describes worst-case performance.
Common complexities: O(1), O(log n), O(n), O(n log n), O(n²).

Sorting Algorithms:
Bubble sort compares adjacent elements repeatedly.
Merge sort divides array and merges sorted halves.
Quick sort uses pivot partitioning for efficiency.

Search Algorithms:
Linear search checks each element sequentially.
Binary search requires sorted data and halves search space each iteration.
        """
    },

    # ============= Mathematics =============
    "calculus_intro": {
        "title": "Introduction to Calculus",
        "category": "📐 Mathematics",
        "icon": "∫",
        "content": """
Calculus is the mathematical study of continuous change, divided into differential and integral calculus.

Limits:
Limits describe the behavior of functions as inputs approach specific values.
They form the foundation for derivatives and integrals.
A limit exists when function values approach a single number from both directions.

Derivatives:
Derivatives measure instantaneous rates of change.
The derivative of a function at a point represents the slope of the tangent line.
Common rules include power rule, product rule, quotient rule, and chain rule.
Applications include finding maximum and minimum values, optimization problems, and motion analysis.

Integration:
Integrals calculate accumulated quantities and areas under curves.
Definite integrals have specific bounds and produce numerical values.
Indefinite integrals represent families of functions and include constants of integration.
The fundamental theorem of calculus connects derivatives and integrals.

Applications:
Physics: velocity, acceleration, force, and energy calculations.
Economics: marginal cost, revenue, and profit analysis.
Engineering: optimization, signal processing, and control systems.
Biology: population growth models and epidemiology.

Techniques of Integration:
Substitution method simplifies integrands by changing variables.
Integration by parts uses the product rule in reverse.
Partial fractions decompose rational functions.
Trigonometric substitution handles expressions with square roots.
        """
    },

    "linear_algebra": {
        "title": "Linear Algebra Fundamentals",
        "category": "📐 Mathematics",
        "icon": "📊",
        "content": """
Linear algebra studies vector spaces, linear transformations, matrices, and systems of linear equations.

Vectors:
Vectors represent quantities with magnitude and direction.
Vector operations include addition, subtraction, and scalar multiplication.
Dot product measures vector similarity and computes projections.
Cross product produces vectors perpendicular to two given vectors.

Matrices:
Matrices are rectangular arrays of numbers organized in rows and columns.
Matrix operations include addition, multiplication, and transposition.
The determinant indicates if a matrix is invertible and measures transformation scaling.
Matrix inverse reverses linear transformations when it exists.

Systems of Linear Equations:
Systems can be solved using elimination, substitution, or matrix methods.
Gaussian elimination reduces matrices to row echelon form.
Solutions may be unique, infinite, or nonexistent depending on equation relationships.

Eigenvalues and Eigenvectors:
Eigenvectors maintain direction under linear transformation, only scaling by eigenvalues.
They reveal fundamental properties of transformations.
Applications include stability analysis, principal component analysis, and quantum mechanics.

Vector Spaces:
Abstract vector spaces generalize geometric vectors.
Basis vectors span the space and are linearly independent.
Dimension counts the number of basis vectors needed.
Subspaces are vector spaces contained within larger spaces.

Applications:
Computer graphics and 3D transformations.
Machine learning and data science.
Quantum computing and physics.
Engineering and signal processing.
        """
    },

    # ============= Physics =============
    "newtons_laws": {
        "title": "Newton's Laws of Motion",
        "category": "🔬 Physics",
        "icon": "🍎",
        "content": """
Newton's three laws of motion describe the relationship between objects and forces.

First Law - Law of Inertia:
An object at rest stays at rest, and an object in motion continues with constant velocity unless acted upon by an external force.
Inertia is the tendency of objects to resist changes in motion.
Mass measures the amount of inertia an object possesses.

Second Law - F = ma:
The acceleration of an object is directly proportional to the net force and inversely proportional to its mass.
Force equals mass times acceleration (F = ma).
Greater forces produce greater accelerations.
More massive objects accelerate less under the same force.

Third Law - Action and Reaction:
For every action, there is an equal and opposite reaction.
Forces always occur in pairs acting on different objects.
The forces are equal in magnitude and opposite in direction.

Applications:
Rocket propulsion uses expelling gases to generate thrust.
Walking involves pushing backward on the ground while the ground pushes forward.
Car acceleration results from tires pushing backward on the road.

Force Types:
Gravitational force attracts objects with mass.
Normal force acts perpendicular to surfaces.
Friction opposes motion between contacting surfaces.
Tension transmits force through ropes and cables.
Applied forces result from direct contact or pushes and pulls.

Problem Solving:
Draw free body diagrams showing all forces.
Resolve forces into components along chosen axes.
Apply Newton's second law to find unknown quantities.
Check answer reasonableness and units.
        """
    },

    # ============= Biology =============
    "cell_biology": {
        "title": "Introduction to Cell Biology",
        "category": "🧬 Biology",
        "icon": "🔬",
        "content": """
Cell biology studies the structure, function, and behavior of cells, the basic units of life.

Cell Theory:
All living organisms are composed of one or more cells.
The cell is the basic unit of life and organization.
All cells arise from pre-existing cells through division.

Prokaryotic Cells:
Lack membrane-bound nucleus and organelles.
Include bacteria and archaea.
Have circular DNA in nucleoid region.
Smaller and simpler than eukaryotic cells.

Eukaryotic Cells:
Contain membrane-bound nucleus and organelles.
Found in animals, plants, fungi, and protists.
Have linear DNA organized in chromosomes.
Larger and more complex internal organization.

Major Organelles:
Nucleus stores genetic information and controls cell activities.
Mitochondria generate ATP through cellular respiration.
Endoplasmic reticulum synthesizes proteins and lipids.
Golgi apparatus modifies, packages, and distributes molecules.
Lysosomes digest cellular waste and foreign materials.
Ribosomes synthesize proteins from amino acids.

Cell Membrane:
Phospholipid bilayer controls substance movement.
Selectively permeable allowing specific molecules through.
Contains proteins for transport, recognition, and signaling.

Cellular Processes:
Photosynthesis converts light energy to chemical energy in plants.
Cellular respiration breaks down glucose to produce ATP.
Cell division creates new cells through mitosis and meiosis.
Protein synthesis translates genetic code into functional proteins.

Cell Communication:
Chemical signals coordinate cellular activities.
Receptors detect external signals and trigger responses.
Signal transduction pathways amplify and process information.
        """
    },

    "genetics_basics": {
        "title": "Fundamentals of Genetics",
        "category": "🧬 Biology",
        "icon": "🧬",
        "content": """
Genetics is the study of heredity and variation in living organisms.

DNA Structure:
DNA is a double helix composed of nucleotides.
Each nucleotide contains a sugar, phosphate, and nitrogenous base.
Four bases: Adenine pairs with Thymine, Guanine pairs with Cytosine.
Base pairing rules enable accurate DNA replication.

Genes and Chromosomes:
Genes are segments of DNA that code for proteins or RNA.
Chromosomes are organized DNA structures containing many genes.
Humans have 23 pairs of chromosomes in most cells.
Sex chromosomes (X and Y) determine biological sex.

Mendelian Genetics:
Traits are inherited through discrete units (genes).
Dominant alleles mask recessive alleles in heterozygotes.
Law of segregation: allele pairs separate during gamete formation.
Law of independent assortment: genes for different traits segregate independently.

DNA Replication:
DNA unwinds and separates into two strands.
Each strand serves as template for new complementary strand.
Enzymes like DNA polymerase synthesize new DNA.
Results in two identical DNA molecules.

Protein Synthesis:
Transcription copies DNA sequence into messenger RNA.
RNA processing removes introns and adds caps.
Translation converts mRNA sequence into amino acid chain.
Ribosomes read codons and assemble proteins.

Mutations:
Changes in DNA sequence caused by errors or environmental factors.
Point mutations affect single nucleotides.
Insertions and deletions shift reading frame.
Can be harmful, beneficial, or neutral.

Genetic Variation:
Sexual reproduction shuffles genetic material.
Crossing over exchanges DNA between chromosomes.
Random fertilization combines different gametes.
Mutations introduce new genetic variations.
        """
    },

    # ============= Chemistry =============
    "atomic_structure": {
        "title": "Atomic Structure and Periodic Table",
        "category": "⚗️ Chemistry",
        "icon": "⚛️",
        "content": """
Atomic structure explains the composition and organization of atoms, the building blocks of matter.

Subatomic Particles:
Protons carry positive charge and reside in the nucleus.
Neutrons have no charge and reside in the nucleus with protons.
Electrons carry negative charge and orbit the nucleus in shells.
Atomic number equals the number of protons.
Mass number equals protons plus neutrons.

Electron Configuration:
Electrons occupy specific energy levels or shells.
Each shell can hold a maximum number of electrons.
First shell holds 2, second holds 8, third holds 18 electrons.
Electrons fill lowest energy levels first.

Valence Electrons:
Outermost electrons participate in chemical bonding.
Determine chemical properties and reactivity.
Elements in the same group have similar valence configurations.

Periodic Table Organization:
Elements arranged by increasing atomic number.
Rows (periods) indicate number of electron shells.
Columns (groups) share similar chemical properties.
Metals on the left, nonmetals on the right, metalloids in between.

Periodic Trends:
Atomic radius decreases across a period, increases down a group.
Ionization energy increases across a period, decreases down a group.
Electronegativity increases across a period, decreases down a group.

Chemical Bonding:
Ionic bonds form through electron transfer between metals and nonmetals.
Covalent bonds form through electron sharing between nonmetals.
Metallic bonds involve delocalized electrons in metal lattices.

Isotopes:
Atoms of same element with different neutron numbers.
Same atomic number, different mass numbers.
May be stable or radioactive.
Used in medical imaging, carbon dating, and nuclear energy.
        """
    },

    # ============= History =============
    "world_war_2": {
        "title": "World War II Overview",
        "category": "📜 History",
        "icon": "🌍",
        "content": """
World War II was a global conflict from 1939 to 1945 involving most nations.

Causes:
Treaty of Versailles created resentment in Germany.
Rise of totalitarian regimes in Germany, Italy, and Japan.
Economic depression and nationalism fueled militarism.
Failure of League of Nations to prevent aggression.

Major Powers:
Axis Powers: Germany, Italy, Japan and their allies.
Allied Powers: United Kingdom, Soviet Union, United States, France, China.

European Theater:
Germany invaded Poland in September 1939, starting the war.
Blitzkrieg tactics enabled rapid German conquests.
Battle of Britain prevented German invasion of England.
Operation Barbarossa: German invasion of Soviet Union.
D-Day invasion liberated Western Europe.
Germany surrendered in May 1945.

Pacific Theater:
Japan invaded China and Southeast Asia.
Pearl Harbor attack brought United States into war.
Island-hopping campaign advanced toward Japan.
Atomic bombs dropped on Hiroshima and Nagasaki.
Japan surrendered in August 1945.

Holocaust:
Systematic genocide of six million Jews by Nazi Germany.
Millions of others murdered including Roma, disabled, and political prisoners.
Concentration and extermination camps across Europe.
Liberation revealed the full horror of Nazi atrocities.

Consequences:
Over 70 million deaths worldwide.
United Nations founded to prevent future conflicts.
Cold War emerged between United States and Soviet Union.
Decolonization movements in Asia and Africa.
Nuclear age began with lasting geopolitical implications.

Technological Impact:
Advances in aviation, radar, and computers.
Development of nuclear weapons.
Medical improvements including antibiotics and blood transfusions.
        """
    },

    # ============= Literature =============
    "shakespeare": {
        "title": "William Shakespeare and His Works",
        "category": "📚 Literature",
        "icon": "🎭",
        "content": """
William Shakespeare was an English playwright and poet, widely regarded as the greatest writer in English literature.

Life and Times:
Born in 1564 in Stratford-upon-Avon, England.
Married Anne Hathaway and had three children.
Moved to London and joined theater companies.
Wrote plays performed at Globe Theatre.
Died in 1616, leaving lasting literary legacy.

Major Tragedies:
Hamlet explores revenge, madness, and mortality.
Macbeth examines ambition, guilt, and fate.
Romeo and Juliet portrays ill-fated young love.
Othello addresses jealousy, manipulation, and racism.
King Lear depicts family conflict and madness.

Comedies:
A Midsummer Night's Dream features magic and mistaken identities.
Much Ado About Nothing explores wit and courtship.
The Merchant of Venice combines comedy with serious themes.
As You Like It celebrates love and pastoral life.

Historical Plays:
Henry V portrays idealized warrior king.
Richard III depicts ruthless rise to power.
Julius Caesar explores political ambition and betrayal.

Literary Techniques:
Invented numerous words and phrases still used today.
Mastered iambic pentameter and blank verse.
Used soliloquies to reveal character thoughts.
Employed wordplay, metaphors, and dramatic irony.

Themes:
Love in various forms and complications.
Power, ambition, and political intrigue.
Appearance versus reality and deception.
Fate, free will, and human nature.
Justice, mercy, and moral dilemmas.

Legacy:
Works translated into every major language.
Influenced countless writers, artists, and thinkers.
Plays continuously performed worldwide.
Enriched English language and cultural heritage.
Provided timeless insights into human experience.
        """
    }
}

def get_all_categories():
    """الحصول على جميع الفئات المتاحة"""
    categories = set()
    for item in KNOWLEDGE_BASE.values():
        categories.add(item['category'])
    return sorted(list(categories))

def get_topics_by_category(category):
    """الحصول على المواضيع حسب الفئة"""
    topics = []
    for key, item in KNOWLEDGE_BASE.items():
        if item['category'] == category:
            topics.append({
                'id': key,
                'title': item['title'],
                'icon': item['icon']
            })
    return topics

def get_topic_content(topic_id):
    """الحصول على محتوى موضوع معين"""
    if topic_id in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[topic_id]
    return None

def search_topics(query):
    """البحث في المواضيع"""
    query = query.lower()
    results = []
    for key, item in KNOWLEDGE_BASE.items():
        if query in item['title'].lower() or query in item['content'].lower():
            results.append({
                'id': key,
                'title': item['title'],
                'category': item['category'],
                'icon': item['icon']
            })
    return results