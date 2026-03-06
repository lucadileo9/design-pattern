# Notes on "An Empirical Study on Maintainability Index of Software Design Patterns"

**Author:** Mahmoud O. Elish (2025)
**Link:** https://ieeexplore.ieee.org/document/11154571

## Section 1: Introduction

Design patterns are considered valuable tools for improving software quality, but scientific literature reports limited empirical evidence on how they impact maintainability in practice.

### The Maintainability Index (MI)

The paper uses the Maintainability Index (MI), originally invented by Oman and Hagemeister and refined by Microsoft (implemented in Visual Studio), with a score scaled from 0 to 100. The formula cross-references three values:

1. **Cyclomatic Complexity (CC):** number of decision paths (if, else, switch)
2. **Halstead Volume (HV):** algorithmic measure of operators and operands used
3. **Lines of Code (LOC):** physical length of the code

The study applies this formula to 17 GoF patterns analyzing five open-source systems (including JHotDraw and JUnit), evaluating the index at three levels: general design, pattern categories, and individual patterns.

## Section 2: Related Works

Summary of related work:

- **Trade-offs (Prechelt et al.):** patterns offer flexibility without increasing maintenance time, but in some cases introduced negative effects (increased complexity, error-proneness).
- **Single pattern successes:** Kurmangali et al. demonstrate positive impact of Abstract Factory and Decorator on maintainability. Al-Obeidallah et al. show the same for Adapter.
- **Human factor (Ng et al.):** prior exposure/knowledge of a specific program significantly affects efficiency; mere theoretical knowledge of patterns does not.

## Section 3: The Empirical Study

### Research Questions

- **RQ1 (Design Level):** do classes with design patterns have higher MI than classes without?
- **RQ2 (Category Level):** are there significant differences between Creational, Structural, and Behavioral patterns?
- **RQ3 (Pattern Level):** which specific patterns achieve the highest MI?

### Dataset and setup

Five open-source systems in Java: JHotDraw (v5.1), JUnit (v3.7), Lexi (v0.1.1 alpha), Nutch (v0.4), PMD (v1.8).

- 868 total classes, ~27.4% with design patterns (63 instances of 17 GoF patterns)
- MI calculated with SonarQube (community edition)
- Patterns verified via P-Mart repository

### Results

#### RQ1: Pattern vs no pattern

Classes with design patterns have statistically higher MI:

- Mean with pattern: **76.21** vs without: **71.88**
- Lower standard deviation with pattern (22.16 vs 28.71) — more consistent quality
- Mann-Whitney U test: p-value = 0.0116 (significant difference)

Patterns enforce modularity, separation of concerns, and encapsulation, reducing cyclomatic complexity.
However, a doubt naturally arises: does it make sense to compare maintainability indices of classes with patterns to those without WITHIN THE SAME SYSTEM? 
The fact that a pattern was applied in one class could make other classes simpler, and thus have higher MI, precisely because the pattern shifted complexity to a specific point.

#### RQ2: Comparison between categories

- **Structural:** highest average (75.21)
- **Creational:** (72.35) — no significant difference from Structural
- **Behavioral:** plummet to 54.8 with high variability (std. dev. 34.33)

Behavioral patterns (Observer, Command, etc.) manage communication between objects, generating tangled control flows and superior algorithmic complexity; consequently, lower MI compared to patterns focusing on static structures or object creation is predictable.

#### RQ3: Patterns with highest MI

Top three: **Builder**, **State**, and **Adapter**.

- **Adapter:** low coupling; changes don't cascade.
- **Builder:** separates creation from representation, avoiding massive constructors.
- **State:** isolates behavior per state in separate classes, eliminating chains of if-else/switch-case.

## Section 4: Conclusions

Based on 63 instances of 17 GoF patterns in five real systems:

1. **Classes with design patterns have significantly higher MI** than those without.
2. **Creational and Structural patterns** demonstrate superior maintainability compared to Behavioral ones.
3. **Builder, State, and Adapter** are the patterns with the highest MI overall.

### Limitations and future work

- Expand analysis to other languages (not just Java) and commercial software.
- Explore the impact of patterns on other attributes: performance and security in particular.

