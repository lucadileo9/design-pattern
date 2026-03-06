# Notes on "Impact of design patterns on software quality: a systematic literature review"

**Authors:** Fadi Wedyan, Somia Abufakher (2019)
**Link:** https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/iet-sen.2018.5446

## Section 1: Introduction

GoF design patterns (creational, structural, and behavioral) were created to solve recurring problems in software design. Classical theory suggests they improve design decisions, facilitate communication among developers, increase maintainability and reusability, and save time and costs.

However, when researchers began measuring these benefits in the field, they obtained strongly contradictory results. For example: some studies conclude that Abstract Factory improves extensibility, others that it has a negative impact. There is little consensus on the actual impact of design patterns on software quality.

**Study objective:** explain these contradictory results by analyzing confounding factors, programming practices, metrics used, and implementation issues. This is done through a Systematic Literature Review (SLR) of studies published between 2000 and 2018.

Contrasting results stem from:

- **Differences in study design:** experiments conducted with different methodologies, difficult to compare.
- **Non-standardized metrics:** different quality attributes, different metrics, applied to different code portions. If one measures bugs and another measures lines of code changed, conclusions about the Factory pattern won't align.
- **Ignored confounding factors:** programmer experience, class size, etc. influence code quality independently of the pattern used.

## Section 2: Related Work

Previous works are reviewed (Weiss, Zhang and Budgen, Ampatzoglou, Ali and Elish, Riaz, Mayvan).

It emerges that it is extremely difficult to compare past empirical findings due to differences in study design and execution. Results have limited generalizability.

**Added value of this paper:** it is the most recent and comprehensive, includes both analytical and empirical approaches, covers all quality attributes and all GoF patterns. The real difference is that it clearly identifies confounding factors and analyzes differences in metrics and software artifacts measured.

## Section 3: Methodology

The review follows the Systematic Literature Review (SLR) method: a scientific means to identify, evaluate, and interpret available research objectively and reproducibly.

### Research Questions

- **RQ1:** What confounding factors, practices, or programming constructs influence quality attributes when using design patterns?
- **RQ2:** Which quality attributes are evaluated, what is measured, and which metrics are used?
- **RQ3:** What are common threats to validity reported in primary studies?

### Selection Process

Search string applied to 5 digital libraries (ACM, IEEE, Science@Direct, SpringerLink, Wiley).

Inclusion/exclusion criteria to go from 804 to 75 articles:

- Only peer-reviewed articles indexed in Scopus
- Only studies on 23 GoF patterns applied to OO software (Java, C#, C++)
- Only articles in English
- For duplicate publications (conference + journal), only journal version retained

### Quality Assessment

To reduce from 75 to 50 articles, evaluation based on 4 factors:

- **F1:** Clear and relevant objectives?
- **F2:** Methodology clearly described?
- **F3:** Metrics specified and mathematically calculated?
- **F4:** Limitations and threats to validity discussed honestly?

In case of disagreement, second round of discussion with external reviewers.

### Data Extraction

From 50 primary studies extracted:

1. **General information:** date, publication venue, number of pages
2. **Detailed information:** patterns investigated, quality attributes, metrics, methodology, limitations

## Section 4: Study Characteristics

### Research Methods

Of 50 studies: 42 empirical, 8 analytical (based on synthetic examples).

- **Case Studies (27 studies)**: Most commonly used method. Researchers take real software (often open-source), analyze it, and observe what happens to classes using patterns during software evolution. Java is the dominant language in these studies.
- **Controlled Experiments (14 studies)**: Laboratory settings are created. Two groups of programmers are taken; one is given code with patterns and the other without, and they are asked to make modifications while measuring time and bugs introduced.
- **Surveys**: Very rare (only 1 main study and some post-experiment questionnaires). They consist of collecting standardized information from a specific population of developers via questionnaires. However, this method suffers from a reliability problem in software engineering: it is very difficult to select a scientifically valid sample of developers, making results complex to generalize.
- **Analytical (8 studies)**: As mentioned, do not use real programmers but analyze code mathematically or conceptually using ad-hoc synthetic examples.

**Note on controlled experiments:** in most cases subjects are university students. Only in 4 out of 14 did professional engineers participate. This affects the validity of results on patterns judged "too complex."

### Dataset

JHotDraw is used in 9 different studies because patterns within it are officially documented.
When patterns are not documented, Design Pattern Mining Tools are needed:

1. **Tsantalis Tool** (12 studies): based on Similarity Scoring Algorithm (SSA), transforms structures and code into graphs and compares similarity scores. Drawback: does not distinguish patterns with identical static structure (e.g., Adapter/Command, State/Strategy).
2. **DeMIMA** (3 studies): multilevel approach with static and dynamic models of Java code. Recognizes 16 GoF patterns.
3. **PINOT:** uses both static analysis and knowledge of behavioral aspects of patterns.

General problem: these tools generate false positives or miss patterns. Studying the same software (JHotDraw) reduces generalizability.

### Most Studied Patterns

- **Creational:** Factory Method (29 evaluations), Singleton (23)
- **Structural:** Composite (28), Decorator (28), Adapter (25)
- **Behavioral:** Observer (31), State (30), Strategy (27)

Almost ignored patterns: Facade, Flyweight, Chain of Responsibility, Interpreter, Iterator, Mediator, Memento (≤ 6 evaluations).

Causes of disparity:

1. **JHotDraw effect:** if dataset contains many Observer patterns and few Flyweight, science studies Observer more
2. **Tool limitation:** recognize certain patterns well but not others
3. **Subject experience:** in controlled tests it is simpler to ask to implement a Singleton than an Interpreter

## Section 5: Results

### RQ1: What confounding factors, practices, or programming constructs influence quality attributes when using design patterns?

#### Documentation

Documentation is fundamental for understanding and maintenance. Controlled experiments show that explicitly documenting pattern instances significantly reduces maintenance time and errors.

- No clear winner between graphical documentation (UML) and textual (code comments): both valid.
- More experienced programmers paradoxically benefit more from pattern documentation than junior developers.

Important risk: "unintentional" patterns (structures resembling a pattern created accidentally, without documentation) make code very difficult to understand.

#### Module Size

The real confounding factor is often not the pattern but class size (Class Size). Huge modules tend to be difficult to maintain and error-prone. So what happens is that a pattern (e.g., Factory) is applied to manage complexity, the class grows because it accumulates responsibilities, becomes difficult to maintain, and one incorrectly concludes it's the pattern's fault.

- Classes participating in design patterns tend to undergo frequent changes.
- Posnett et al. demonstrated that it is class size that explains the tendency to change, more than the role in the pattern.

Open question: do classes become huge because of certain patterns (e.g., Singleton which tends to increase size) or due to developers' additional responsibilities?

#### Crosscutting Concerns

Some patterns (e.g., Observer) require that many classes be aware of their existence — transverse logic that scatters everywhere and tangles with business logic.

The Degree of Scattering (DOS) induced by patterns reduces modularity, making software difficult to modify and increasing defect probability.

Proposed solution: **Aspect-Oriented Programming (AOP)**.

- Languages like AspectJ allow extracting transverse logic into constructs called Aspects.
- Hannemann and Kiczales, Garcia et al. demonstrate that implementing GoF patterns with AOP improves separation of concerns, cohesion, reduces coupling and code size.
- AO implementation makes pattern code reusable in half of cases.

However, AOP introduces technical challenges and adoption barriers that limit its widespread use.

### RQ2: Which quality attributes are evaluated, what is measured, and which metrics are used?

#### Maintainability

Most studied attribute. Science measures it by evaluating:

- **Change Proneness:** how often a class is modified between versions. Classes with patterns change often, but the reasons matter: bug fix (negative) or new feature easily added (positive)? Many studies don't make this distinction.
- **Fault Proneness / Defect Frequency:** do patterns cause bugs? Totally contradictory results — some studies say more bugs, others fewer (structural patterns seem safer). Often depends on developer inexperience or lack of documentation.
- **Stability:** measured via Ripple Effect Measurement (REM) — probability that a modification propagates in cascade. Classes with patterns tend to be more stable.

#### Performance and Energy

Performance is rarely studied in relation to patterns. Recent studies measured energy consumption:

- For simple problems, solutions without patterns consume less energy.
- Patterns become more energy efficient on large and complex modules.

#### QMOOD

The QMOOD model (Quality Model for Object-Oriented Design) evaluates quality during the design phase, measuring 6 attributes through internal metrics (cohesion, coupling, size):

1. Effectiveness
2. Extendibility
3. Flexibility
4. Functionality
5. Reusability
6. Understandability

Results: GoF patterns generally improve reusability and flexibility, but each pattern has a different level and the effect changes if used in a standalone app or a library.

### RQ3: What are common threats to validity reported in primary studies?

#### Construct Validity

Do the metrics actually measure what they claim?

- **Tool accuracy:** pattern mining tools make errors (false positives/negatives). If the tool is wrong, all subsequent measurements are unreliable.
- **Change measurement:** counting modifications without distinguishing bug fixes from feature additions is misleading.
- **Social bias:** in questionnaires programmers tend to respond to "look good."

#### Internal Validity

Is it really the pattern causing the observed effect?

Problems in controlled experiments:

- Cheating and communication between subjects in control and experimental groups
- Mortality (test abandonment) and fatigue
- Temporal precedence: statistical correlation does not prove causality. Did the pattern cause bugs, or was it inserted to try to fix pre-existing bugs?

#### External Validity

Do results hold outside the study context?

- **Students vs. professionals:** vast majority of experiments use students. Real development is teamwork; tests evaluate isolated individuals.
- **Java and JHotDraw monopoly:** almost exclusively Java, always the same open-source software.

#### Replicability

To repeat an experiment, datasets, code, tools and statistical formulas must be public. Many historical studies did not do this.

## Section 6: Study Limitations

The authors criticize their own work:

1. **Construct validity:** risk of missing important studies. Mitigated by searching 5 digital libraries with very strict criteria and cross-checked manual evaluations.
2. **Internal validity:** risk in data extraction (different studies calling the same metric by different names). Mitigated with two-phase independent process.
3. **External validity:** the generalizability of the review is limited by the generalizability of primary studies included.

## Section 7: Conclusions

### Documentation

Definitive empirical evidence: documenting design pattern instances has a positive effect on understanding and maintainability. Developers should add this documentation, even just as code comments. Future research should also address unintentional patterns.

### Class Size

Module size massively influences all quality attributes. Unresolved question: does using certain patterns require larger classes, or do classes grow due to business responsibilities?

### Modularity and AOP

OO patterns are difficult to isolate in a module due to dependencies. AOP showed promising results but suffers from problems preventing widespread adoption. New ways to improve pattern modularity are needed.

### Metric Chaos

Maintainability is the most evaluated attribute but has been measured in the most disparate ways (change proneness, fault proneness, stability, different models). This generated contradictory results and limits comparability between studies.

