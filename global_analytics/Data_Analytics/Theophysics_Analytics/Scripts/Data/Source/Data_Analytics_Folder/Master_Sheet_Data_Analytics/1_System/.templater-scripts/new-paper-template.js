// New Paper Template Script
async function newPaper(tp) {
    // Get paper details
    const paperNum = await tp.system.prompt("Paper number (e.g., 14)");
    const paperTitle = await tp.system.prompt("Paper title");
    const paperSubtitle = await tp.system.prompt("Paper subtitle (optional)");
    
    if (!paperNum || !paperTitle) {
        new Notice('Paper number and title required!');
        return '';
    }
    
    // Select paper category
    const category = await tp.system.suggester(
        ['Foundation', 'Mathematical', 'Validation', 'Synthesis'],
        ['foundation', 'mathematical', 'validation', 'synthesis'],
        false,
        "Select paper category"
    );
    
    // Select relevant χ variables
    const chiVars = ['Grace', 'MutualInfo', 'Entropy', 'SelfReference', 'Time', 
                     'Knowledge', 'Relationality', 'Quantum', 'Force', 'Coherence'];
    const selectedVars = await tp.system.suggester(
        chiVars,
        chiVars,
        true,
        "Select relevant χ variables"
    );
    
    // Build tags
    const tags = [
        'pillar/physics',
        'pillar/mathematics',
        `paper/P${paperNum}_${paperTitle.toUpperCase().replace(/\s+/g, '_').substring(0, 20)}`
    ];
    
    if (selectedVars) {
        tags.push(...selectedVars.map(v => `χ_var/${v}`));
    }
    
    // Generate template
    const template = `---
tags: [${tags.join(', ')}]
paper_id: P${paperNum}_${paperTitle.toUpperCase().replace(/\s+/g, '_')}
paper_number: ${paperNum}
title: "${paperTitle}"
subtitle: "${paperSubtitle || ''}"
category: ${category}
status: draft
date: ${tp.date.now("YYYY-MM-DD")}
author: David Lowe
---

# Paper #${paperNum}: ${paperTitle}

${paperSubtitle ? `## ${paperSubtitle}` : ''}

---

## Abstract

<!-- 200-300 word summary -->

---

## I. Introduction

### Background

### Problem Statement

### Proposed Solution

---

## II. Theoretical Framework

### Core Concepts

### Mathematical Formulation

### Connection to Master Equation

---

## III. Detailed Analysis

### Component 1

### Component 2

### Component 3

---

## IV. Implications

### For Physics

### For Theology

### For Philosophy

---

## V. Testable Predictions

1. **Prediction 1**: 
2. **Prediction 2**: 
3. **Prediction 3**: 

---

## VI. Conclusion

### Summary

### Future Work

---

## References

1. 
2. 
3. 

---

## Appendices

### Appendix A: Mathematical Derivations

### Appendix B: Supporting Data

---

**Status**: ${category} layer paper
**Next Steps**: Complete theoretical framework
**Related Papers**: [[Paper-${parseInt(paperNum) - 1}]], [[Paper-${parseInt(paperNum) + 1}]]
`;
    
    new Notice(`Paper #${paperNum} template created!`);
    return template;
}

module.exports = newPaper;
