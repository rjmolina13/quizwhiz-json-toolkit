#!/usr/bin/env python3
"""
QuizWhiz JSON Toolkit - All-in-One QuizWhiz JSON Management Tool

A comprehensive tool that combines MHTML extraction, JSON merging, and QuizWhiz backup management
into a single application with both CLI and GUI interfaces.

Features:
- Extract quiz data from Google Forms MHTML files
- Merge multiple quiz JSON files
- Merge quiz data with QuizWhiz backup files
- Both command-line and graphical user interfaces

Author: RubyJ/@rjmolina13
"""

# Application version
VERSION = "4.4.4"

import re
import quopri
import json
from datetime import datetime
import sys
import os
import argparse
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import platform
import subprocess

# ANSI color codes for better CLI experience
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print a welcome banner"""
    current_year = datetime.now().year
    
    # Calculate padding for centering the version text
    version_text = f"QuizWhiz JSON Toolkit v{VERSION}"
    total_width = 62  # Width inside the box borders
    version_padding = (total_width - len(version_text)) // 2
    version_line = f"║{' ' * version_padding}{version_text}{' ' * (total_width - len(version_text) - version_padding)}║"
    
    banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
{version_line}
║           All-in-One QuizWhiz JSON Management Tool           ║
║                                                              ║
║           (c) {current_year} RubyJ, made with ♡ for lablab             ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """
    print(banner)

# ============================================================================
# ENHANCED DIFFICULTY ANALYSIS WITH NLP
# ============================================================================

def analyze_question_difficulty(question_text, options, correct_answer):
    """
    Enhanced difficulty analysis using context reading and simple NLP techniques.
    Analyzes question structure, cognitive complexity, and semantic content.
    Trained on LET General Education and Professional Education question patterns.
    """
    
    # Normalize text for analysis
    question_lower = question_text.lower().strip()
    
    # Initialize scoring system
    difficulty_score = 0
    
    # 1. COGNITIVE COMPLEXITY ANALYSIS (Bloom's Taxonomy) - Enhanced with LET patterns
    cognitive_indicators = {
        'remember': {
            'keywords': [
                # Basic recall patterns from LET data
                'what is', 'who is', 'when did', 'where is', 'define', 'identify', 'list', 'name', 'recall', 'state', 'recognize',
                'the date of', 'the title', 'the author of', 'the capital of', 'the largest', 'the smallest',
                'known as', 'called', 'refers to', 'means', 'stands for', 'acronym for',
                # Enhanced recall patterns from Professional Education
                'which of the following is', 'what does', 'who developed', 'what theory', 'what law',
                'according to', 'based on', 'the term', 'this refers to', 'is defined as'
            ],
            'score': 1
        },
        'understand': {
            'keywords': [
                # Comprehension patterns from LET data
                'explain', 'describe', 'summarize', 'interpret', 'classify', 'compare', 'contrast', 'illustrate', 'translate',
                'the essence of', 'the purpose of', 'the meaning of', 'demonstrates', 'shows', 'indicates',
                'example of', 'characteristic of', 'feature of', 'belongs to',
                # Enhanced comprehension patterns
                'what is meant by', 'this means that', 'the concept of', 'understanding of',
                'the principle behind', 'the idea that', 'represents', 'symbolizes'
            ],
            'score': 2
        },
        'apply': {
            'keywords': [
                # Application patterns from LET data
                'calculate', 'solve', 'demonstrate', 'use', 'apply', 'implement', 'execute', 'operate', 'practice',
                'find the value', 'compute', 'determine', 'obtain', 'perform', 'simplify',
                'what score must', 'if the student has', 'the simple interest on', 'the total amount after',
                # Enhanced application patterns from Professional Education
                'what teaching strategy', 'what method should', 'how would you', 'what approach',
                'in this situation', 'the teacher should', 'what would be the best', 'how can the teacher'
            ],
            'score': 3
        },
        'analyze': {
            'keywords': [
                # Analysis patterns from LET data
                'analyze', 'examine', 'investigate', 'categorize', 'differentiate', 'distinguish', 'organize', 'deconstruct',
                'what kind of thinking', 'what type of', 'which approach', 'what strategy',
                'based on information', 'according to', 'in relation to',
                # Enhanced analysis patterns
                'what factor', 'what element', 'what component', 'break down', 'dissect',
                'what causes', 'what leads to', 'relationship between', 'connection between'
            ],
            'score': 4
        },
        'evaluate': {
            'keywords': [
                # Evaluation patterns from LET data
                'evaluate', 'assess', 'critique', 'judge', 'justify', 'argue', 'defend', 'support', 'validate', 'rate',
                'most appropriate', 'best', 'most effective', 'least', 'cannot be considered',
                'which of the following can be', 'what went wrong', 'is the teacher right',
                # Enhanced evaluation patterns
                'most suitable', 'least appropriate', 'not recommended', 'should not',
                'priority should be', 'first consideration', 'primary concern', 'main focus'
            ],
            'score': 5
        },
        'create': {
            'keywords': [
                # Creation patterns from LET data
                'create', 'design', 'develop', 'construct', 'formulate', 'generate', 'produce', 'synthesize', 'compose',
                'make research', 'developing a system', 'design the instructional', 'plan ahead for',
                # Enhanced creation patterns
                'establish', 'build', 'organize', 'structure', 'arrange', 'set up',
                'plan a lesson', 'design a curriculum', 'develop a program', 'create a strategy'
            ],
            'score': 6
        }
    }
    
    # Check cognitive complexity
    max_cognitive_score = 0
    for level, data in cognitive_indicators.items():
        for keyword in data['keywords']:
            if keyword in question_lower:
                max_cognitive_score = max(max_cognitive_score, data['score'])
    
    difficulty_score += max_cognitive_score
    
    # 2. QUESTION STRUCTURE ANALYSIS
    structure_indicators = {
        'simple_factual': {
            'patterns': [
                r'what is the', r'who is', r'when did', r'where is', r'which of the following is',
                r'the name of', r'the largest', r'the smallest', r'the first', r'the last',
                r'how many', r'what type of', r'what kind of', r'which one', r'the capital of',
                r'the author of', r'the date of', r'the title of'
            ],
            'score': 1
        },
        'multiple_concepts': {
            'patterns': [
                r'both.*and', r'either.*or', r'not only.*but also', r'as well as', r'in addition to',
                r'all of the following', r'none of the following', r'except for', r'with the exception of',
                r'along with', r'together with'
            ],
            'score': 2
        },
        'conditional_reasoning': {
            'patterns': [
                r'if.*then', r'assuming that', r'given that', r'provided that', r'in case of',
                r'when.*will', r'unless.*otherwise', r'suppose that', r'what would happen if',
                r'under what conditions'
            ],
            'score': 3
        },
        'comparative_analysis': {
            'patterns': [
                r'compare.*with', r'contrast.*and', r'difference between', r'similarity between', r'versus',
                r'most appropriate', r'best describes', r'most suitable', r'least likely',
                r'most effective', r'better than', r'worse than', r'unlike.*', r'whereas.*',
                r'on the other hand', r'in contrast to'
            ],
            'score': 3
        },
        'causal_relationships': {
            'patterns': [
                r'because of', r'due to', r'as a result of', r'leads to', r'causes', r'effects of',
                r'results in', r'consequently', r'therefore', r'thus', r'hence',
                r'what factor', r'what causes', r'why does', r'the reason for'
            ],
            'score': 4
        },
        'application_scenarios': {
            'patterns': [
                r'in the classroom', r'teaching strategy', r'learning activity',
                r'instructional approach', r'assessment method', r'what should.*do',
                r'how would you', r'the teacher should', r'students should',
                r'in this situation', r'given this scenario', r'what teaching strategy',
                r'what is meant by', r'what approach'
            ],
            'score': 4
        }
    }
    
    # Check question structure
    max_structure_score = 0
    for structure_type, data in structure_indicators.items():
        for pattern in data['patterns']:
            if re.search(pattern, question_lower):
                max_structure_score = max(max_structure_score, data['score'])
    
    difficulty_score += max_structure_score
    
    # 3. DOMAIN-SPECIFIC COMPLEXITY - Enhanced with LET-specific patterns
    domain_complexity = {
        'basic_facts': {
            'keywords': [
                # Basic factual knowledge from LET General Education
                'capital', 'flag', 'anthem', 'hero', 'date', 'year', 'name of', 'title of',
                'archipelago', 'blood compact', 'ilustrados', 'aetas', 'balagtasan',
                'commensalism', 'food web', 'genus', 'esters', 'cube', 'exponential form',
                # Enhanced Biology basic facts
                'cell', 'tissue', 'organ', 'system', 'blood', 'heart', 'brain', 'lung',
                'bone', 'muscle', 'skin', 'eye', 'ear', 'nose', 'mouth', 'tooth', 'teeth',
                'ribs', 'sternum', 'vertebral column', 'cerebellum', 'aorta', 'ventricle'
            ],
            'score': 1
        },
        'mathematical_operations': {
            'keywords': [
                # Mathematical concepts from LET data
                'calculate', 'compute', 'solve for', 'find the value', 'equation', 'formula', 'percentage',
                'simplify', 'greatest common', 'least common', 'average score', 'simple interest',
                'consecutive even integers', 'discount', 'final average', 'total amount'
            ],
            'score': 2
        },
        'scientific_principles': {
            'keywords': [
                # Science concepts from LET data
                'principle', 'law', 'theory', 'hypothesis', 'experiment', 'observation', 'phenomenon',
                'citric acid cycle', 'electron configuration', 'carbon family', 'organic compounds',
                'feeding connections', 'life forms', 'biochemical pathway',
                # Enhanced Biology principles
                'mitosis', 'meiosis', 'dna', 'rna', 'protein', 'enzyme', 'hormone', 'chromosome',
                'gene', 'allele', 'phenotype', 'genotype', 'mutation', 'natural selection',
                'adaptation', 'species', 'taxonomy', 'classification', 'kingdom', 'phylum',
                'photosynthesis', 'respiration', 'evolution', 'genetics', 'ecosystem', 'biodiversity',
                'glucagon', 'adrenalin', 'insulin', 'thyroxine', 'leukocytes', 'lymphocytes',
                'erythrocytes', 'cellulose', 'cotyledon', 'hilum', 'meristematic', 'cambium',
                'epidermis', 'tundra', 'rain forest', 'biome', 'habitat'
            ],
            'score': 3
        },
        'educational_theory': {
            'keywords': [
                # Professional education concepts from LET data
                'pedagogy', 'curriculum', 'assessment', 'learning theory', 'teaching method', 'educational philosophy',
                'outcome-based education', 'understanding by design', 'problem-based', 'cooperative learning',
                'affective domain', 'cognitive domain', 'psychomotor domain', 'bloom\'s taxonomy',
                'convergent thinking', 'divergent thinking', 'reflective teaching', 'action research',
                # Enhanced curriculum and theory patterns
                'curriculum development', 'curriculum model', 'curriculum approach', 'delivery modes',
                'learning objectives', 'competency', 'learning materials', 'instructional design',
                'educational approach', 'teaching approach', 'learning approach', 'methodology',
                # Enhanced Professional Education concepts
                'classroom management', 'discipline', 'motivation', 'reinforcement', 'guidance process',
                'test reliability', 'erikson stages', 'maslow hierarchy', 'course objective',
                'learning climate', 'drta', 'cultural heritage', 'test norms', 'professionalization',
                'correlation', 'student motivation', 'higher-order thinking', 'vygotsky scaffolding',
                'real-world connections', 'ict concerns', 'pygmalion effect', 'ripple effect'
            ],
            'score': 5  # Increased from 4 to 5
        },
        'advanced_educational_concepts': {
            'keywords': [
                # Advanced professional education from LET data
                'multicultural perspective', 'inclusive education', 'alternative learning system',
                'intellectual disability', 'direct instruction', 'task analysis', 'systematic feedback',
                'progressivism', 'reconstructionism', 'existentialism', 'behaviorist learning theory',
                'media literacy', 'digital literacy', 'information literacy', 'cyber literacy',
                # Enhanced advanced concepts
                'philosophical foundations', 'educational philosophy', 'constructivist', 'behaviorist',
                'cognitive theory', 'metacognitive', 'scaffolding', 'differentiation', 'taxonomy',
                'reader-response theory', 'modern taxonomy', 'ancient taxonomy', 'inclusivity',
                'enhanced basic education act', 'madrasa curriculum', 'chronological ages',
                # Enhanced philosophical and theoretical concepts
                'perennialism', 'essentialism', 'idealism', 'pragmatism', 'phenomenology',
                'phenomenologists', 'idealists', 'pragmatists', 'plato philosophy',
                'freud psychoanalytic theory', 'chomsky language learning', 'bandura social learning',
                'thorndike law of effect', 'bruner theory', 'trust vs maturity', 'autonomy vs self-doubt',
                'initiative vs guilt', 'behavior modification', 'pleasant consequences'
            ],
            'score': 6  # Increased from 5 to 6
        },
        'research_methodology': {
            'keywords': [
                # Research and advanced concepts
                'research', 'methodology', 'statistical', 'qualitative', 'quantitative', 'meta-analysis',
                'capstone', 'developing a system', 'negatively skewed', 'score distribution',
                'philosophical foundations', 'curriculum process', 'delivery modes',
                # Enhanced research patterns
                'formulation', 'effectiveness', 'evaluation', 'determining objectives', 'model begins',
                'extent of poverty', 'squatter area', 'clusters of major', 'sub-concepts', 'interaction'
            ],
            'score': 7  # Increased from 6 to 7
        }
    }
    
    # Check domain complexity
    max_domain_score = 0
    for domain, data in domain_complexity.items():
        for keyword in data['keywords']:
            if keyword in question_lower:
                max_domain_score = max(max_domain_score, data['score'])
    
    difficulty_score += max_domain_score
    
    # 4. LINGUISTIC COMPLEXITY ANALYSIS
    linguistic_score = 0
    
    # Sentence length complexity
    word_count = len(question_text.split())
    if word_count > 30:
        linguistic_score += 2
    elif word_count > 20:
        linguistic_score += 1
    
    # Technical vocabulary density - Enhanced with LET-specific terms
    technical_terms = [
        # Educational theory terms
        'methodology', 'paradigm', 'epistemology', 'ontology', 'phenomenology',
        'pedagogy', 'andragogy', 'heutagogy', 'constructivism', 'behaviorism',
        'cognitivism', 'metacognition', 'scaffolding', 'differentiation',
        'taxonomy', 'synthesis', 'analysis', 'evaluation', 'application',
        # LET-specific professional terms
        'outcome-based', 'competency-based', 'contextualized', 'deductive', 'inductive',
        'synchronous', 'asynchronous', 'blended learning', 'modular approach',
        'progressivism', 'reconstructionism', 'existentialism', 'idealism',
        'alternative learning system', 'inclusive education', 'multicultural',
        # Enhanced Professional Education terms
        'classroom management', 'instructional design', 'curriculum development',
        'assessment method', 'learning objectives', 'competency-based',
        'erikson stages', 'maslow hierarchy', 'vygotsky scaffolding', 'piaget theory',
        'freud psychoanalytic', 'bandura social learning', 'thorndike law',
        'bruner discovery learning', 'bloom taxonomy', 'gardner multiple intelligence',
        'perennialism', 'essentialism', 'pragmatism', 'phenomenologists',
        'guidance process', 'test reliability', 'correlation coefficient',
        'professionalization', 'pygmalion effect', 'ripple effect',
        # Biology technical terms
        'mitochondria', 'chloroplast', 'ribosome', 'endoplasmic reticulum',
        'golgi apparatus', 'lysosome', 'nucleus', 'cytoplasm', 'membrane',
        'photosynthesis', 'cellular respiration', 'mitosis', 'meiosis',
        'dna replication', 'transcription', 'translation', 'enzyme',
        'protein synthesis', 'amino acid', 'nucleotide', 'chromosome',
        'allele', 'genotype', 'phenotype', 'heredity', 'mutation',
        'ecosystem', 'biodiversity', 'symbiosis', 'parasitism', 'mutualism',
        'commensalism', 'predation', 'competition', 'succession',
        'homeostasis', 'metabolism', 'osmosis', 'diffusion', 'active transport',
        'cerebellum', 'vertebral column', 'sternum', 'glucagon', 'insulin',
        'thyroxine', 'adrenalin', 'leukocytes', 'erythrocytes', 'lymphocytes',
        'cellulose', 'cotyledon', 'hilum', 'meristematic', 'cambium', 'epidermis',
        'tundra', 'biome', 'taxonomy', 'classification', 'binomial nomenclature',
        # Filipino linguistic terms
        'pangatnig', 'paglalapi', 'pagbubuo', 'pagkaltas', 'dugtungan',
        'patotoo', 'pagtanggi', 'talumpati', 'bugtungan'
    ]
    
    technical_count = sum(1 for term in technical_terms if term in question_lower)
    linguistic_score += min(technical_count, 3)  # Cap at 3 points
    
    # Complex sentence structures
    complex_structures = [
        r'not only.*but also', r'although.*however', r'despite.*nevertheless',
        r'whereas.*while', r'in contrast to.*however', r'on the one hand.*on the other hand'
    ]
    
    for pattern in complex_structures:
        if re.search(pattern, question_lower):
            linguistic_score += 1
    
    difficulty_score += linguistic_score
    
    # 5. ANSWER CHOICE COMPLEXITY ANALYSIS
    answer_complexity_score = 0
    
    if options:
        # Check for similar/confusing options
        option_texts = [re.sub(r'^[A-D]\. ', '', opt) for opt in options]
        
        # Calculate average option length
        avg_option_length = sum(len(opt.split()) for opt in option_texts) / len(option_texts)
        if avg_option_length > 10:
            answer_complexity_score += 2
        elif avg_option_length > 5:
            answer_complexity_score += 1
        
        # Check for technical terms in options
        technical_in_options = sum(1 for opt in option_texts 
                                 for term in technical_terms if term.lower() in opt.lower())
        answer_complexity_score += min(technical_in_options, 2)
        
        # Check for numerical/formula complexity in options
        numerical_patterns = [r'\d+\.\d+', r'\d+%', r'\d+/\d+', r'[a-z]\^\d+', r'√\d+']
        for opt in option_texts:
            for pattern in numerical_patterns:
                if re.search(pattern, opt):
                    answer_complexity_score += 1
                    break
    
    difficulty_score += answer_complexity_score
    
    # 6. CONTEXT AND PRIOR KNOWLEDGE REQUIREMENTS
    context_score = 0
    
    # Philippine-specific knowledge - Enhanced with LET context
    philippine_context = [
        'republic act', 'ra ', 'deped', 'ched', 'let', 'licensure examination',
        'k-12', 'mother tongue', 'filipino', 'tagalog', 'cebuano', 'ilokano',
        # Historical context from LET General Education
        'philippine independence', 'diosdado macapagal', 'emilio aguinaldo', 'apolinario mabini',
        'legaspi', 'sikatuna', 'blood compact', 'galleon trade', 'ilustrados',
        'antonio de morga', 'sucesos de las islas filipinas', 'spanish regime',
        # Geographic and cultural context
        'luzon', 'pampanga', 'tarlac', 'zambales', 'aetas', 'igorots', 'mangyans',
        'archipelago', 'bohol', 'pasig', 'magallanes ave'
    ]
    
    for context in philippine_context:
        if context in question_lower:
            context_score += 1
    
    # Educational law and policy knowledge - Enhanced with LET specifics
    educational_law = [
        'ra 10533', 'ra 7836', 'ra 9155', 'enhanced basic education act',
        'magna carta', 'code of ethics', 'professional standards',
        # LET-specific educational policies
        'code of ethics for professional teachers', 'philippine education plan',
        'curriculum development', 'educational landscape', 'teaching-learning process',
        'school governance', 'borderless global society', 'multicultural perspective'
    ]
    
    for law in educational_law:
        if law in question_lower:
            context_score += 2
    
    difficulty_score += min(context_score, 4)  # Cap at 4 points
    
    # 7. HARD QUESTION PATTERN DETECTION - Based on actual LET hard questions
    hard_question_patterns = {
        'complex_teaching_strategies': {
            'patterns': [
                r'what teaching strategy.*employ',
                r'i\. .*ii\. .*iii\. .*iv\.',  # Roman numeral options
                r'socio-drama.*dilemma.*jury trial.*parliamentary',
                r'effectively analyze and evaluate evidence',
                r'critical thinking and problem solving',
                r'competency.*effectively analyze.*evaluate.*evidence.*arguments.*claims.*beliefs'
            ],
            'score': 12  # Increased from 10
        },
        'media_literacy_analysis': {
            'patterns': [
                r'ability to access.*analyze.*evaluate.*create.*act',
                r'using all forms of communication',
                r'literacy.*21st century.*access.*analyze.*evaluate.*create.*act',
                r'analyze.*evaluate.*evidence.*arguments.*claims.*beliefs',
                r'media literacy.*information literacy.*digital literacy.*cyber literacy',
                r'literacy.*21st century.*refers to the ability'
            ],
            'score': 12  # Increased from 10
        },
        'complex_multiple_choice': {
            'patterns': [
                r'i, ii, iii and iv',
                r'ii, iii and iv only',
                r'i and ii only',
                r'i, ii and iv only',
                r'which of the following.*except',
                r'all.*except one',
                r'only.*i\. .*ii\. .*iii\. .*iv\.'
            ],
            'score': 10  # Increased from 8
        },
        'advanced_educational_theory': {
            'patterns': [
                r'philosophical foundations.*curriculum',
                r'progressivists.*john dewey',
                r'behaviorist learning theory',
                r'bronfenbrenner.*ecological theory',
                r'vygotsky.*zone of proximal development',
                # Enhanced educational theory patterns
                r'curriculum development model.*begins.*determining.*objectives',
                r'reader-response theory',
                r'modern taxonomy.*carolus linnaeus.*ancient taxonomy',
                r'enhanced basic education act.*inclusivity',
                r'madrasa curriculum.*inclusive education'
            ],
            'score': 11  # Increased from 9
        },
        'curriculum_and_assessment_complexity': {
            'patterns': [
                r'curriculum process.*delivery modes.*applied',
                r'extent of poverty.*squatter area',
                r'approach.*topics.*clusters.*major.*sub-concepts.*interaction',
                r'additional learning experiences.*learners.*gifts.*talents.*chronological ages',
                r'competency.*grade.*math.*interprets data.*bar graphs',
                r'diversity of learners.*competency.*teacher display',
                r'formulation.*basic education curriculum.*ra 10533.*inclusivity',
                # Enhanced curriculum patterns
                r'test item analysis.*difficulty index.*discrimination index',
                r'guidance process.*counseling.*psychological testing',
                r'test reliability.*validity.*correlation coefficient',
                r'course objective.*assessment.*learning outcomes',
                r'positive learning climate.*classroom management',
                r'cultural heritage.*multicultural perspective'
            ],
            'score': 11  # Increased from 10
        },
        'biology_complexity': {
            'patterns': [
                r'cellular respiration.*mitochondria.*atp production',
                r'photosynthesis.*chloroplast.*light reactions.*calvin cycle',
                r'dna replication.*transcription.*translation.*protein synthesis',
                r'mitosis.*meiosis.*chromosome.*genetic variation',
                r'ecosystem.*food chain.*energy flow.*nutrient cycling',
                r'homeostasis.*feedback mechanisms.*regulation',
                r'evolution.*natural selection.*adaptation.*speciation',
                r'genetics.*alleles.*genotype.*phenotype.*inheritance',
                r'anatomy.*physiology.*organ systems.*structure.*function',
                r'taxonomy.*classification.*binomial nomenclature.*phylogeny'
            ],
            'score': 12
        },
        'philosophical_education_complexity': {
            'patterns': [
                r'existentialism.*perennialism.*progressivism.*essentialism',
                r'phenomenologists.*idealists.*pragmatists.*philosophy',
                r'plato.*aristotle.*socrates.*philosophical foundations',
                r'erikson.*stages.*trust.*autonomy.*initiative.*identity',
                r'freud.*psychoanalytic.*unconscious.*defense mechanisms',
                r'piaget.*cognitive development.*stages.*schema.*assimilation',
                r'vygotsky.*zone of proximal development.*scaffolding.*social learning',
                r'bandura.*social learning theory.*modeling.*observational learning',
                r'thorndike.*law of effect.*behaviorism.*conditioning',
                r'bruner.*discovery learning.*spiral curriculum.*cognitive theory'
            ],
            'score': 13
        },
        'specific_hard_indicators': {
            'patterns': [
                r'refers to the ability to access, analyze, evaluate, create and act',
                r'intend my students to attain competency',
                r'teaching strategy will i need to employ',
                r'21st century.*ability.*access.*analyze.*evaluate.*create.*act',
                # Enhanced specific indicators
                r'what competency must the teacher display',
                r'which learning materials are most appropriate.*master the competency',
                r'what does inclusivity mean',
                r'curriculum development model.*effectiveness',
                # Professional Education specific indicators
                r'pygmalion effect.*teacher expectations.*student performance',
                r'ripple effect.*classroom discipline.*behavior management',
                r'maslow.*hierarchy.*needs.*motivation.*self-actualization',
                r'bloom.*taxonomy.*cognitive.*affective.*psychomotor.*domains',
                r'gardner.*multiple intelligence.*learning styles.*individual differences',
                # Biology specific indicators
                r'structure.*function.*relationship.*biological systems',
                r'compare.*contrast.*biological processes.*mechanisms',
                r'analyze.*interpret.*experimental data.*scientific method',
                r'predict.*outcomes.*based on.*biological principles'
            ],
            'score': 15  # Increased from 14
        }
    }
    
    # Check for hard question patterns
    hard_pattern_score = 0
    for pattern_type, data in hard_question_patterns.items():
        for pattern in data['patterns']:
            if re.search(pattern, question_lower):
                hard_pattern_score = max(hard_pattern_score, data['score'])
                break
    
    difficulty_score += hard_pattern_score
    
    # 8. FINAL DIFFICULTY CLASSIFICATION - Refined based on LET patterns
    # Normalize score to 0-100 scale
    # Updated max scores: cognitive(6) + structure(4) + domain(7) + linguistic(6) + answer(4) + context(4) + hard_patterns(15)
    max_possible_score = 6 + 4 + 7 + 6 + 4 + 4 + 15  # Sum of max scores from each category (updated)
    normalized_score = (difficulty_score / max_possible_score) * 100
    
    # LET-specific difficulty classification based on observed patterns:
    # Easy: Basic recall, simple calculations, factual knowledge (0-35%)
    # Medium: Application of concepts, analysis of scenarios, educational theory (35-50%)
    # Hard: Complex evaluation, synthesis, advanced professional concepts, complex teaching strategies (50%+)
    
    if normalized_score >= 45:  # Further lowered threshold for hard questions
        return "hard"
    elif normalized_score >= 25:  # Lowered threshold for medium questions
        return "medium"
    else:
        return "easy"

# ============================================================================
# MHTML EXTRACTION FUNCTIONALITY
# ============================================================================

def extract_quiz_from_mhtml(mhtml_file, deck_name, output_file, verbose=False, progress_callback=None):
    """Extract quiz data from MHTML file and save to JSON file"""
    
    if progress_callback:
        progress_callback("Reading MHTML file...")
    
    if verbose:
        print(f"\n{Colors.OKCYAN}Starting extraction process...{Colors.ENDC}")
        print(f"Input file: {mhtml_file}")
        print(f"Output file: {output_file}")
        print(f"Deck name: {deck_name}\n")
    
    # Read and extract HTML from MHTML
    try:
        with open(mhtml_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        error_msg = f"Error reading file: {e}"
        if verbose:
            print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
        return None, error_msg

    if progress_callback:
        progress_callback("Extracting HTML content...")

    # Extract HTML content
    html_match = re.search(r'Content-Type: text/html.*?\n\n(.*?)(?=\n--)', content, re.DOTALL)
    if html_match:
        html_content = html_match.group(1)
        # Decode quoted-printable
        try:
            decoded_html = quopri.decodestring(html_content.encode()).decode('utf-8', errors='ignore')
        except Exception as e:
            error_msg = f"Error decoding HTML content: {e}"
            if verbose:
                print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
            return None, error_msg
    else:
        error_msg = f"Could not extract HTML from {mhtml_file}"
        if verbose:
            print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
        return None, error_msg

    if progress_callback:
        progress_callback("Finding question blocks...")

    # Find all question blocks using the Qr7Oae class with role="listitem" pattern
    question_block_pattern = r'<div[^>]*class="[^"]*Qr7Oae[^"]*"[^>]*role="listitem"[^>]*>.*?(?=<div[^>]*class="[^"]*Qr7Oae[^"]*"[^>]*role="listitem"|$)'
    question_blocks = re.findall(question_block_pattern, decoded_html, re.DOTALL)
    
    if verbose:
        print(f"{Colors.OKGREEN}Found {len(question_blocks)} question blocks{Colors.ENDC}")
    
    if len(question_blocks) == 0:
        error_msg = "No questions found in the file. Please check if this is a valid Google Forms MHTML file."
        if verbose:
            print(f"{Colors.WARNING}{error_msg}{Colors.ENDC}")
        return None, error_msg
    
    quiz_data = {
        "quizwhiz_quizzes": []
    }
    
    current_time = datetime.now().isoformat() + 'Z'
    
    if progress_callback:
        progress_callback(f"Processing {len(question_blocks)} questions...")
    
    for i, question_block in enumerate(question_blocks):
        if progress_callback:
            progress_callback(f"Processing question {i+1}/{len(question_blocks)}...")
        
        # Extract question text from M7eMe span (improved to handle nested spans)
        question_text = None
        m7eme_start = re.search(r'<span[^>]*class="[^"]*M7eMe[^"]*"[^>]*>', question_block)
        if m7eme_start:
            start_pos = m7eme_start.end()
            # Count nested spans to find the correct closing tag
            content = question_block[start_pos:]
            span_count = 1
            pos = 0
            while span_count > 0 and pos < len(content):
                next_open = content.find('<span', pos)
                next_close = content.find('</span>', pos)
                
                if next_close == -1:
                    break
                if next_open != -1 and next_open < next_close:
                    span_count += 1
                    pos = next_open + 5
                else:
                    span_count -= 1
                    if span_count == 0:
                        raw_text = content[:next_close]
                        # Clean and process the extracted text
                        question_text = re.sub(r'<[^>]+>', '', raw_text).strip()
                        question_text = re.sub(r'\s+', ' ', question_text)
                        question_text = re.sub(r'&nbsp;', ' ', question_text)
                        question_text = question_text.strip()
                        question_text = re.sub(r'^[\\"]+|[\\"]+$', '', question_text)
                        question_text = re.sub(r'^\s+|\s+$', '', question_text)
                        # Remove question numbers from the beginning (e.g., "1. ", "2. ", etc.)
                        question_text = re.sub(r'^\d+\.\s*', '', question_text)
                        break
                    pos = next_close + 7
        
        # Fallback if M7eMe extraction failed
        if not question_text:
            question_text = f"Question {i+1}"
        
        # Extract all options using aDTYNe class pattern
        option_pattern = r'<span[^>]*class="[^"]*aDTYNe[^"]*"[^>]*>([^<]+)</span>'
        all_options = re.findall(option_pattern, question_block)
        
        # Filter and clean options (should be A., B., C., D. or A), B), C), D) format)
        options = []
        for option in all_options:
            clean_option = re.sub(r'\s+', ' ', option.strip())
            clean_option = re.sub(r'^[\\"]+|[\\"]+$', '', clean_option)
            clean_option = re.sub(r'^\s+|\s+$', '', clean_option)
            # Accept any non-empty option that isn't a duplicate
            if clean_option and clean_option not in options:
                options.append(clean_option)
        
        # Sort options by letter
        options.sort(key=lambda x: x[0] if x and len(x) > 0 else 'Z')
        
        if not options:
            if verbose:
                print(f"{Colors.WARNING}No options found for question {i+1}, skipping...{Colors.ENDC}")
            continue
            
        # Detect correct answer using the patterns
        correct_answer = ""
        wrong_answers = []
        
        # Step 1: Check if question was answered correctly or incorrectly
        answer_status_patterns = [
            (r'<div class="fKfAyc">\s*Tama\s*</div>', 'correct'),
            (r'<div class="fKfAyc">\s*Correct\s*</div>', 'correct'),
            (r'<div class="fKfAyc">\s*Mali\s*</div>', 'incorrect'),
            (r'<div class="fKfAyc">\s*Incorrect\s*</div>', 'incorrect')
        ]
        
        question_status = None
        status_match_position = -1
        
        for pattern, status in answer_status_patterns:
            match = re.search(pattern, question_block, re.IGNORECASE)
            if match:
                question_status = status
                status_match_position = match.start()
                break
        
        if question_status == 'correct':
            # If answered correctly, find the option closest to the "Correct" indicator
            if status_match_position >= 0:
                search_start = max(0, status_match_position - 1000)
                search_end = min(len(question_block), status_match_position + 1000)
                search_window = question_block[search_start:search_end]
                
                closest_option = None
                closest_distance = float('inf')
                
                for option in options:
                    option_pos = search_window.find(option)
                    if option_pos >= 0:
                        status_pos_in_window = status_match_position - search_start
                        distance = abs(option_pos - status_pos_in_window)
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_option = option
                
                if closest_option:
                    correct_answer = closest_option
        
        elif question_status == 'incorrect':
            # If answered incorrectly, look for the "Correct answer" section
            correct_answer_section_patterns = [
                r'<div class="fD9txe"[^>]*role="heading"[^>]*aria-level="3"[^>]*>\s*Tamang sagot\s*</div>',
                r'<div class="fD9txe"[^>]*role="heading"[^>]*aria-level="3"[^>]*>\s*Correct answer\s*</div>'
            ]
            
            for pattern in correct_answer_section_patterns:
                section_match = re.search(pattern, question_block, re.IGNORECASE)
                if section_match:
                    after_section = question_block[section_match.end():]
                    
                    for option in options:
                        if option in after_section[:2000]:
                            correct_answer = option
                            break
                    
                    if correct_answer:
                        break
        
        # Fallback methods if the above didn't work
        if not correct_answer:
            # Method 1: Look for aria-checked="true" pattern
            checked_pattern = r'aria-checked="true"[^>]*data-value="([^"]+)"'
            checked_match = re.search(checked_pattern, question_block)
            if checked_match:
                checked_value = checked_match.group(1)
                for option in options:
                    if checked_value in option or option in checked_value:
                        correct_answer = option
                        break
        
        if not correct_answer:
            # Method 2: Look for aria-label="Correct" indicators
            correct_indicators = [
                r'aria-label="Correct"',
                r'aria-label="Tama"'
            ]
            
            for indicator in correct_indicators:
                correct_matches = list(re.finditer(indicator, question_block, re.IGNORECASE))
                for match in correct_matches:
                    start_pos = max(0, match.start() - 1000)
                    end_pos = min(len(question_block), match.end() + 1000)
                    search_window = question_block[start_pos:end_pos]
                    
                    for option in options:
                        if option in search_window:
                            option_pos = search_window.find(option)
                            indicator_pos = search_window.find(match.group(0))
                            if abs(option_pos - indicator_pos) < 500:
                                correct_answer = option
                                break
                        if correct_answer:
                            break
                    if correct_answer:
                        break
                if correct_answer:
                    break
        
        # Default to first option if still not found
        if not correct_answer and options:
            correct_answer = options[0]
            if verbose:
                print(f"{Colors.WARNING}Warning: Could not determine correct answer for question {i+1}, defaulting to first option{Colors.ENDC}")
        
        # All other options are wrong
        wrong_answers = [opt for opt in options if opt != correct_answer]
        
        # Enhanced difficulty detection with context reading and simple NLP
        difficulty = analyze_question_difficulty(question_text, options, clean_correct if 'clean_correct' in locals() else correct_answer)
        
        # Remove option letters (A., B., etc. or (A), (B), etc.) from answers for cleaner format (uppercase and lowercase)
        clean_correct = re.sub(r'^\([A-Da-d]\)\s*|^[A-Da-d][\.)\]]\s*', '', correct_answer) if correct_answer else ""
        clean_wrong = [re.sub(r'^\([A-Da-d]\)\s*|^[A-Da-d][\.)\]]\s*', '', ans) for ans in wrong_answers]
        
        # Additional cleaning for answers
        if clean_correct:
            clean_correct = re.sub(r'^[\\"]+|[\\"]+$', '', clean_correct.strip())
        clean_wrong = [re.sub(r'^[\\"]+|[\\"]+$', '', ans.strip()) for ans in clean_wrong]
        
        quiz_item = {
            "id": str(int(datetime.now().timestamp() * 1000) + i),
            "deck": deck_name,
            "question": question_text,
            "correctAnswer": clean_correct,
            "wrongAnswers": clean_wrong,
            "difficulty": difficulty,
            "createdAt": current_time
        }
        
        quiz_data["quizwhiz_quizzes"].append(quiz_item)
        
        if verbose:
            print(f"{Colors.OKCYAN}Question {i+1}:{Colors.ENDC} {question_text[:50]}...")
            print(f"  Status: {question_status or 'unknown'}")
            print(f"  Options: {len(options)}")
            print(f"  Correct: {clean_correct}")
            print(f"  Wrong: {len(clean_wrong)} options")
            print()
    
    if progress_callback:
        progress_callback("Removing duplicates...")
    
    # Data cleanup: Remove duplicate questions based on question text
    if verbose:
        print(f"\n{Colors.OKCYAN}Performing data cleanup...{Colors.ENDC}")
    
    original_count = len(quiz_data["quizwhiz_quizzes"])
    
    # Track seen questions and keep unique ones
    seen_questions = set()
    unique_quizzes = []
    duplicates_removed = 0
    
    def normalize_question_text(text):
        """Normalize question text for duplicate detection"""
        normalized = text.strip().lower()
        normalized = re.sub(r'_{2,}', '_____', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = re.sub(r'[""''`]', '', normalized)
        return normalized
    
    for quiz_item in quiz_data["quizwhiz_quizzes"]:
        normalized_question = normalize_question_text(quiz_item["question"])
        
        if normalized_question not in seen_questions:
            seen_questions.add(normalized_question)
            unique_quizzes.append(quiz_item)
        else:
            duplicates_removed += 1
            if verbose:
                print(f"  {Colors.WARNING}Removed duplicate: {quiz_item['question'][:60]}...{Colors.ENDC}")
    
    # Update quiz data with unique questions only
    quiz_data["quizwhiz_quizzes"] = unique_quizzes
    final_count = len(unique_quizzes)
    
    # Calculate difficulty statistics
    difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
    for quiz_item in unique_quizzes:
        difficulty = quiz_item.get("difficulty", "easy")
        if difficulty in difficulty_stats:
            difficulty_stats[difficulty] += 1
    
    if verbose:
        print(f"\n{Colors.OKGREEN}Data cleanup complete:{Colors.ENDC}")
        print(f"  Original questions: {original_count}")
        print(f"  Duplicates removed: {duplicates_removed}")
        print(f"  Final unique questions: {final_count}")
        print(f"\n{Colors.OKCYAN}Difficulty Distribution:{Colors.ENDC}")
        print(f"  Easy: {Colors.OKGREEN}{difficulty_stats['easy']}{Colors.ENDC} questions")
        print(f"  Medium: {Colors.WARNING}{difficulty_stats['medium']}{Colors.ENDC} questions")
        print(f"  Hard: {Colors.FAIL}{difficulty_stats['hard']}{Colors.ENDC} questions")
    
    if progress_callback:
        progress_callback("Saving JSON file...")
    
    # Save to JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        
        success_msg = f"Extraction complete! Created {output_file} with {final_count} questions (Easy: {difficulty_stats['easy']}, Medium: {difficulty_stats['medium']}, Hard: {difficulty_stats['hard']})"
        if verbose:
            print(f"\n{Colors.OKGREEN}✓ Extraction complete!{Colors.ENDC}")
            print(f"Created: {Colors.BOLD}{output_file}{Colors.ENDC}")
            print(f"Questions: {Colors.BOLD}{final_count}{Colors.ENDC}")
            print(f"Deck: {Colors.BOLD}{deck_name}{Colors.ENDC}")
        
        if progress_callback:
            progress_callback("Extraction completed successfully!")
        
        return quiz_data, success_msg
        
    except Exception as e:
        error_msg = f"Error saving file: {e}"
        if verbose:
            print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
        return None, error_msg

# ============================================================================
# JSON MERGING FUNCTIONALITY
# ============================================================================

def load_quiz_file(file_path, verbose=False):
    """Load and validate a quiz JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate structure
        if 'quizwhiz_quizzes' not in data:
            if verbose:
                print(f"Warning: {file_path} doesn't have 'quizwhiz_quizzes' key. Skipping.")
            return None
        
        if not isinstance(data['quizwhiz_quizzes'], list):
            if verbose:
                print(f"Warning: {file_path} 'quizwhiz_quizzes' is not a list. Skipping.")
            return None
        
        if verbose:
            print(f"Loaded {len(data['quizwhiz_quizzes'])} questions from {os.path.basename(file_path)}")
        return data['quizwhiz_quizzes']
    
    except FileNotFoundError:
        if verbose:
            print(f"Error: File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        if verbose:
            print(f"Error: Invalid JSON in {file_path}: {e}")
        return None
    except Exception as e:
        if verbose:
            print(f"Error loading {file_path}: {e}")
        return None

def merge_quiz_files(file_paths, output_file=None, verbose=False, progress_callback=None):
    """Merge multiple quiz files into one"""
    merged_quizzes = []
    total_questions = 0
    
    if verbose:
        print(f"\nMerging {len(file_paths)} files...")
        print("=" * 50)
    
    if progress_callback:
        progress_callback(f"Merging {len(file_paths)} files...")
    
    for i, file_path in enumerate(file_paths):
        if progress_callback:
            progress_callback(f"Loading file {i+1}/{len(file_paths)}: {os.path.basename(file_path)}")
        
        if not os.path.exists(file_path):
            if verbose:
                print(f"Warning: File does not exist: {file_path}")
            continue
        
        quizzes = load_quiz_file(file_path, verbose)
        if quizzes:
            merged_quizzes.extend(quizzes)
            total_questions += len(quizzes)
    
    if not merged_quizzes:
        error_msg = "No valid quiz data found in any of the files."
        if verbose:
            print(f"Error: {error_msg}")
        return None, error_msg
    
    # Create output structure
    merged_data = {
        "quizwhiz_quizzes": merged_quizzes
    }
    
    # Generate output filename with timestamp if not provided
    if not output_file:
        current_time = datetime.now()
        timestamp = current_time.strftime("%Y%m%d_%H%M%S")
        output_file = f"quizwhiz_export_{timestamp}.json"
        
        # Use directory of the first valid input file
        first_valid_file = next((f for f in file_paths if os.path.exists(f)), None)
        if first_valid_file:
            output_dir = os.path.dirname(os.path.abspath(first_valid_file))
            output_file = os.path.join(output_dir, output_file)
    
    if progress_callback:
        progress_callback("Saving merged file...")
    
    # Save merged file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
        
        success_msg = f"Merge completed! Total questions: {total_questions}, Output: {output_file}"
        if verbose:
            print(f"\nMerge completed successfully!")
            print(f"Total questions merged: {total_questions}")
            print(f"Output file: {output_file}")
            print(f"File size: {os.path.getsize(output_file) / 1024:.1f} KB")
        
        if progress_callback:
            progress_callback("Merge completed successfully!")
        
        return output_file, success_msg
    
    except Exception as e:
        error_msg = f"Error saving merged file: {e}"
        if verbose:
            print(f"Error: {error_msg}")
        return None, error_msg

# ============================================================================
# QUIZWHIZ BACKUP MERGING FUNCTIONALITY
# ============================================================================

def validate_json_file(file_path, file_type="JSON"):
    """Validate if file exists and is a valid JSON file"""
    if not os.path.exists(file_path):
        return False, f"{file_type} file not found: {file_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, "Valid JSON file"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in {file_type} file: {e}"
    except Exception as e:
        return False, f"Error reading {file_type} file: {e}"

def merge_quizwhiz_files(backup_file, quiz_file, output_file, append_mode=False, verbose=False, progress_callback=None):
    """Merge QuizWhiz files by replacing or appending quizwhiz_quizzes content"""
    
    if progress_callback:
        progress_callback("Starting QuizWhiz merge...")
    
    if verbose:
        print(f"\n{Colors.OKCYAN}Starting merge process...{Colors.ENDC}")
        print(f"Backup file (target): {backup_file}")
        print(f"Quiz file (source): {quiz_file}")
        print(f"Output file: {output_file}\n")
    
    try:
        if progress_callback:
            progress_callback("Loading backup file...")
        
        # Load backup file (target)
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        if verbose:
            print(f"{Colors.OKGREEN}✓ Loaded backup file successfully{Colors.ENDC}")
            if 'quizwhiz_quizzes' in backup_data:
                print(f"  Current quizzes in backup: {len(backup_data['quizwhiz_quizzes'])}")
            else:
                print(f"  {Colors.WARNING}Warning: No 'quizwhiz_quizzes' found in backup file{Colors.ENDC}")
        
        if progress_callback:
            progress_callback("Loading quiz file...")
        
        # Load quiz file (source)
        with open(quiz_file, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
        
        if verbose:
            print(f"{Colors.OKGREEN}✓ Loaded quiz file successfully{Colors.ENDC}")
            if 'quizwhiz_quizzes' in quiz_data:
                print(f"  New quizzes to merge: {len(quiz_data['quizwhiz_quizzes'])}")
            else:
                error_msg = "No 'quizwhiz_quizzes' found in quiz file"
                if verbose:
                    print(f"  {Colors.FAIL}Error: {error_msg}{Colors.ENDC}")
                return False, error_msg
        
        # Validate that quiz file has quizwhiz_quizzes
        if 'quizwhiz_quizzes' not in quiz_data:
            error_msg = "Source file does not contain 'quizwhiz_quizzes' array"
            return False, error_msg
        
        if progress_callback:
            progress_callback(f"Performing {'append' if append_mode else 'replace'} operation...")
        
        # Perform the merge
        original_count = len(backup_data.get('quizwhiz_quizzes', []))
        source_count = len(quiz_data['quizwhiz_quizzes'])
        
        if append_mode:
            # Append new quizzes to existing ones
            if 'quizwhiz_quizzes' not in backup_data:
                backup_data['quizwhiz_quizzes'] = []
            backup_data['quizwhiz_quizzes'].extend(quiz_data['quizwhiz_quizzes'])
            final_count = len(backup_data['quizwhiz_quizzes'])
        else:
            # Replace quizwhiz_quizzes content
            backup_data['quizwhiz_quizzes'] = quiz_data['quizwhiz_quizzes']
            final_count = source_count
        
        # Update export metadata if it exists
        if 'exportDate' in backup_data:
            backup_data['exportDate'] = datetime.now().isoformat() + 'Z'
        
        if 'exportVersion' in backup_data:
            backup_data['exportVersion'] = '2.1'  # Increment version to indicate merge
        
        if verbose:
            print(f"\n{Colors.OKCYAN}Merge operation completed:{Colors.ENDC}")
            print(f"  Mode: {'Append' if append_mode else 'Replace'}")
            print(f"  Original quizzes: {original_count}")
            print(f"  Source quizzes: {source_count}")
            print(f"  Final quizzes: {final_count}")
            if append_mode:
                print(f"  Added: +{source_count}")
            else:
                print(f"  Change: {'+' if final_count > original_count else ''}{final_count - original_count}")
            
            # Show other preserved data structures
            other_keys = [key for key in backup_data.keys() if key != 'quizwhiz_quizzes']
            if other_keys:
                print(f"  Preserved data structures: {', '.join(other_keys)}")
        
        if progress_callback:
            progress_callback("Saving merged file...")
        
        # Save merged file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        success_msg = f"QuizWhiz merge complete! Total quizzes: {final_count}"
        if append_mode:
            success_msg += f" (Added: +{source_count})"
        elif original_count != final_count:
            change = final_count - original_count
            success_msg += f" (Change: {'+' if change > 0 else ''}{change})"
        
        if verbose:
            print(f"\n{Colors.OKGREEN}✓ Merge complete!{Colors.ENDC}")
            print(f"Created: {Colors.BOLD}{output_file}{Colors.ENDC}")
            print(f"Total quizzes: {Colors.BOLD}{final_count}{Colors.ENDC}")
            
            if append_mode:
                print(f"Added: {Colors.BOLD}+{source_count} quizzes{Colors.ENDC}")
            elif original_count != final_count:
                change_text = f"({'+' if final_count > original_count else ''}{final_count - original_count} from original)"
                print(f"Change: {Colors.BOLD}{change_text}{Colors.ENDC}")
        
        if progress_callback:
            progress_callback("QuizWhiz merge completed successfully!")
        
        return True, success_msg
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format - {e}"
        return False, error_msg
    except Exception as e:
        error_msg = f"Error during merge: {e}"
        return False, error_msg

# ============================================================================
# JSON TRANSFORMER FUNCTIONALITY
# ============================================================================

def transform_json_structure(source_file, output_file, backup_file=None, append_mode=False, apply_nlp=True, verbose=False, progress_callback=None):
    """
    Transform existing JSON structure and optionally merge with QuizWhiz backup.
    Applies NLP difficulty classification to the final output.
    
    Args:
        source_file (str): Path to source JSON file
        output_file (str): Path to output file
        backup_file (str, optional): Path to QuizWhiz backup file
        append_mode (bool): Whether to append to backup (vs replace)
        apply_nlp (bool): Whether to apply NLP difficulty classification
        verbose (bool): Whether to show verbose output
        progress_callback (callable, optional): Progress callback function
    
    Returns:
        tuple: (success, message)
    """
    try:
        if progress_callback:
            progress_callback("Loading source file...")
        
        # Load source file
        with open(source_file, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
        
        if verbose:
            print(f"{Colors.OKGREEN}✓ Loaded source file successfully{Colors.ENDC}")
        
        # Validate and normalize source data structure
        if progress_callback:
            progress_callback("Validating source structure...")
        
        transformed_quizzes = []
        
        # Handle different possible source structures
        if 'quizwhiz_quizzes' in source_data:
            # Already in QuizWhiz format
            transformed_quizzes = source_data['quizwhiz_quizzes']
            if verbose:
                print(f"  Source format: QuizWhiz format ({len(transformed_quizzes)} questions)")
        elif isinstance(source_data, list):
            # Array of questions
            transformed_quizzes = source_data
            if verbose:
                print(f"  Source format: Question array ({len(transformed_quizzes)} questions)")
        elif 'questions' in source_data:
            # Generic quiz format with 'questions' key
            transformed_quizzes = source_data['questions']
            if verbose:
                print(f"  Source format: Generic quiz format ({len(transformed_quizzes)} questions)")
        else:
            # Try to find any array that looks like questions
            for key, value in source_data.items():
                if isinstance(value, list) and len(value) > 0:
                    # Check if first item looks like a question
                    first_item = value[0]
                    if isinstance(first_item, dict) and ('question' in first_item or 'text' in first_item or 'prompt' in first_item):
                        transformed_quizzes = value
                        if verbose:
                            print(f"  Source format: Custom format with '{key}' key ({len(transformed_quizzes)} questions)")
                        break
            
            if not transformed_quizzes:
                return False, "Could not identify question structure in source file"
        
        if not transformed_quizzes:
            return False, "No questions found in source file"
        
        # Apply NLP difficulty classification if requested
        if apply_nlp:
            if progress_callback:
                progress_callback("Applying NLP difficulty classification...")
            
            if verbose:
                print(f"{Colors.OKCYAN}Applying NLP difficulty classification...{Colors.ENDC}")
            
            for i, question in enumerate(transformed_quizzes):
                if progress_callback and i % 10 == 0:
                    progress_callback(f"Processing question {i+1}/{len(transformed_quizzes)}...")
                
                # Extract question components for analysis
                question_text = ""
                options = []
                correct_answer = ""
                
                # Handle different question formats
                if 'question' in question:
                    question_text = question['question']
                elif 'text' in question:
                    question_text = question['text']
                elif 'prompt' in question:
                    question_text = question['prompt']
                
                if 'options' in question:
                    options = question['options']
                elif 'choices' in question:
                    options = question['choices']
                elif 'answers' in question:
                    options = question['answers']
                
                if 'correct' in question:
                    correct_answer = question['correct']
                elif 'correctAnswer' in question:
                    correct_answer = question['correctAnswer']
                elif 'answer' in question:
                    correct_answer = question['answer']
                
                # Apply difficulty analysis
                difficulty = analyze_question_difficulty(question_text, options, correct_answer)
                question['difficulty'] = difficulty
            
            if verbose:
                # Calculate difficulty statistics
                difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
                for question in transformed_quizzes:
                    difficulty = question.get("difficulty", "easy")
                    if difficulty in difficulty_stats:
                        difficulty_stats[difficulty] += 1
                
                print(f"  Difficulty classification complete:")
                print(f"    Easy: {Colors.OKGREEN}{difficulty_stats['easy']}{Colors.ENDC} questions")
                print(f"    Medium: {Colors.WARNING}{difficulty_stats['medium']}{Colors.ENDC} questions")
                print(f"    Hard: {Colors.FAIL}{difficulty_stats['hard']}{Colors.ENDC} questions")
        
        # Handle backup file integration if provided
        final_data = None
        if backup_file:
            if progress_callback:
                progress_callback("Integrating with backup file...")
            
            if verbose:
                print(f"{Colors.OKCYAN}Integrating with QuizWhiz backup...{Colors.ENDC}")
            
            # Load backup file
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            if verbose:
                print(f"  Loaded backup file with {len(backup_data.get('quizwhiz_quizzes', []))} existing questions")
            
            # Perform integration
            original_count = len(backup_data.get('quizwhiz_quizzes', []))
            source_count = len(transformed_quizzes)
            
            if append_mode:
                # Append new questions to existing ones
                if 'quizwhiz_quizzes' not in backup_data:
                    backup_data['quizwhiz_quizzes'] = []
                backup_data['quizwhiz_quizzes'].extend(transformed_quizzes)
                final_count = len(backup_data['quizwhiz_quizzes'])
            else:
                # Replace quizwhiz_quizzes content
                backup_data['quizwhiz_quizzes'] = transformed_quizzes
                final_count = source_count
            
            # Update metadata
            if 'exportDate' in backup_data:
                backup_data['exportDate'] = datetime.now().isoformat() + 'Z'
            if 'exportVersion' in backup_data:
                backup_data['exportVersion'] = '2.1'
            
            final_data = backup_data
            
            if verbose:
                print(f"  Integration mode: {'Append' if append_mode else 'Replace'}")
                print(f"  Final question count: {Colors.BOLD}{final_count}{Colors.ENDC}")
                if append_mode:
                    print(f"  Added: {Colors.BOLD}+{source_count}{Colors.ENDC} questions")
        else:
            # Create new QuizWhiz format structure
            final_data = {
                "quizwhiz_quizzes": transformed_quizzes,
                "exportDate": datetime.now().isoformat() + 'Z',
                "exportVersion": "2.1"
            }
            final_count = len(transformed_quizzes)
        
        if progress_callback:
            progress_callback("Saving transformed file...")
        
        # Save final file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)
        
        # Generate success message
        success_msg = f"JSON transformation complete! Total questions: {final_count}"
        if backup_file:
            if append_mode:
                success_msg += f" (Added: +{len(transformed_quizzes)})"
            else:
                success_msg += f" (Replaced with {len(transformed_quizzes)} questions)"
        
        if apply_nlp:
            success_msg += " with NLP difficulty classification"
        
        if verbose:
            print(f"\n{Colors.OKGREEN}✓ Transformation complete!{Colors.ENDC}")
            print(f"Created: {Colors.BOLD}{output_file}{Colors.ENDC}")
            print(f"Total questions: {Colors.BOLD}{final_count}{Colors.ENDC}")
            
            if apply_nlp:
                # Show final difficulty breakdown
                difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
                for question in final_data['quizwhiz_quizzes']:
                    difficulty = question.get("difficulty", "easy")
                    if difficulty in difficulty_stats:
                        difficulty_stats[difficulty] += 1
                
                print(f"Final difficulty breakdown:")
                print(f"  Easy: {Colors.OKGREEN}{difficulty_stats['easy']}{Colors.ENDC} questions")
                print(f"  Medium: {Colors.WARNING}{difficulty_stats['medium']}{Colors.ENDC} questions")
                print(f"  Hard: {Colors.FAIL}{difficulty_stats['hard']}{Colors.ENDC} questions")
        
        if progress_callback:
            progress_callback("JSON transformation completed successfully!")
        
        return True, success_msg
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON format - {e}"
        return False, error_msg
    except Exception as e:
        error_msg = f"Error during transformation: {e}"
        return False, error_msg

# ============================================================================
# CLI INTERFACE
# ============================================================================

def cli_workflow():
    """Command-line interface workflow"""
    print_banner()
    print(f"{Colors.OKCYAN}Welcome to QuizWhiz JSON Toolkit CLI!{Colors.ENDC}")
    print("Choose your workflow:\n")
    
    print("1. Complete MHTML Extraction Workflow (Extract → Merge → QuizWhiz Integration)")
    print("2. JSON Transformer (Transform existing JSON + NLP classification)")
    print("3. Exit")
    
    while True:
        choice = input(f"\n{Colors.OKBLUE}Select workflow (1-3): {Colors.ENDC}").strip()
        if choice in ['1', '2', '3']:
            break
        print(f"{Colors.WARNING}Please enter 1, 2, or 3.{Colors.ENDC}")
    
    if choice == '1':
        mhtml_extraction_workflow()
    elif choice == '2':
        json_transformer_workflow()
    elif choice == '3':
        print(f"{Colors.OKCYAN}Goodbye!{Colors.ENDC}")
        return

def mhtml_extraction_workflow():
    """MHTML extraction workflow"""
    print(f"\n{Colors.HEADER}MHTML Extraction Workflow{Colors.ENDC}")
    print("This workflow will guide you through extracting quiz data from MHTML files.\n")
    
    # Step 1: MHTML Extraction
    print(f"{Colors.HEADER}Step 1: Google Forms MHTML Extraction{Colors.ENDC}")
    print("=" * 50)
    
    while True:
        mhtml_file = input(f"{Colors.OKBLUE}Enter the path to your MHTML file: {Colors.ENDC}").strip()
        if not mhtml_file:
            print(f"{Colors.WARNING}Please enter a valid file path.{Colors.ENDC}")
            continue
        
        mhtml_file = os.path.expanduser(mhtml_file)
        mhtml_file = os.path.abspath(mhtml_file)
        
        if not os.path.exists(mhtml_file):
            print(f"{Colors.FAIL}File not found: {mhtml_file}{Colors.ENDC}")
            continue
        
        if not mhtml_file.lower().endswith('.mhtml'):
            print(f"{Colors.WARNING}Warning: File doesn't have .mhtml extension. Continue anyway? (y/n): {Colors.ENDC}", end="")
            if input().lower() != 'y':
                continue
        
        break
    
    while True:
        deck_name = input(f"{Colors.OKBLUE}Enter the deck name: {Colors.ENDC}").strip()
        if deck_name:
            deck_name = re.sub(r'[<>:"/\\|?*]', '_', deck_name)
            break
        print(f"{Colors.WARNING}Please enter a valid deck name.{Colors.ENDC}")
    
    # Generate output filename
    safe_deck_name = re.sub(r'[<>:"/\\|?*]', '_', deck_name)
    extracted_file = f"{safe_deck_name.lower().replace(' ', '_')}.json"
    extracted_file = os.path.abspath(extracted_file)
    
    print(f"\n{Colors.OKCYAN}Extracting quiz data...{Colors.ENDC}")
    result, message = extract_quiz_from_mhtml(mhtml_file, deck_name, extracted_file, verbose=True)
    
    if result is None:
        print(f"{Colors.FAIL}Extraction failed: {message}{Colors.ENDC}")
        return
    
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
    current_file = extracted_file
    
    # Step 2: Optional JSON Merging
    print(f"\n{Colors.HEADER}Step 2: JSON Output Merger (Optional){Colors.ENDC}")
    print("=" * 50)
    
    while True:
        merge_json = input(f"{Colors.OKBLUE}Do you want to merge this output with other quiz JSON files? (y/n): {Colors.ENDC}").strip().lower()
        if merge_json in ['y', 'yes', 'n', 'no']:
            break
        print(f"{Colors.WARNING}Please enter 'y' or 'n'.{Colors.ENDC}")
    
    if merge_json in ['y', 'yes']:
        files_to_merge = [current_file]
        
        print(f"\n{Colors.OKCYAN}Adding additional files to merge:{Colors.ENDC}")
        print("Enter file paths (press Enter after each path, type 'done' when finished)")
        
        while True:
            file_path = input(f"{Colors.OKBLUE}File {len(files_to_merge)}: {Colors.ENDC}").strip()
            
            if file_path.lower() == 'done':
                if len(files_to_merge) < 2:
                    print(f"{Colors.WARNING}Please add at least one more file to merge.{Colors.ENDC}")
                    continue
                break
            
            if not file_path:
                print(f"{Colors.WARNING}Please enter a valid file path or 'done'.{Colors.ENDC}")
                continue
            
            file_path = os.path.expanduser(file_path)
            file_path = os.path.abspath(file_path)
            
            if not os.path.exists(file_path):
                print(f"{Colors.FAIL}File not found: {file_path}{Colors.ENDC}")
                continue
            
            files_to_merge.append(file_path)
            print(f"{Colors.OKGREEN}Added: {os.path.basename(file_path)}{Colors.ENDC}")
        
        # Generate merged filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        merged_file = f"merged_quiz_{timestamp}.json"
        merged_file = os.path.abspath(merged_file)
        
        print(f"\n{Colors.OKCYAN}Merging {len(files_to_merge)} files...{Colors.ENDC}")
        result_file, message = merge_quiz_files(files_to_merge, merged_file, verbose=True)
        
        if result_file is None:
            print(f"{Colors.FAIL}Merge failed: {message}{Colors.ENDC}")
            return
        
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        current_file = result_file
    
    # Step 3: Optional QuizWhiz Backup Merging
    print(f"\n{Colors.HEADER}Step 3: QuizWhiz JSON Backup Merger (Optional){Colors.ENDC}")
    print("=" * 50)
    
    while True:
        merge_backup = input(f"{Colors.OKBLUE}Do you want to merge this with your QuizWhiz backup file? (y/n): {Colors.ENDC}").strip().lower()
        if merge_backup in ['y', 'yes', 'n', 'no']:
            break
        print(f"{Colors.WARNING}Please enter 'y' or 'n'.{Colors.ENDC}")
    
    if merge_backup in ['y', 'yes']:
        while True:
            backup_file = input(f"{Colors.OKBLUE}Enter the path to your QuizWhiz backup JSON file: {Colors.ENDC}").strip()
            if not backup_file:
                print(f"{Colors.WARNING}Please enter a valid file path.{Colors.ENDC}")
                continue
            
            backup_file = os.path.expanduser(backup_file)
            backup_file = os.path.abspath(backup_file)
            
            is_valid, error_msg = validate_json_file(backup_file, "QuizWhiz backup")
            if not is_valid:
                print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
                continue
            
            break
        
        # Ask for merge mode
        print(f"\n{Colors.OKBLUE}Merge mode options:{Colors.ENDC}")
        print("1. Replace - Replace all existing quizzes with new ones")
        print("2. Append - Add new quizzes to existing ones")
        
        while True:
            choice = input(f"{Colors.OKBLUE}Choose merge mode (1 or 2): {Colors.ENDC}").strip()
            if choice in ['1', '2']:
                append_mode = choice == '2'
                break
            print(f"{Colors.WARNING}Please enter 1 or 2.{Colors.ENDC}")
        
        # Generate output filename
        backup_path = Path(backup_file)
        final_output = backup_path.parent / f"{backup_path.stem}_UPDATED.json"
        final_output = str(final_output)
        
        print(f"\n{Colors.OKCYAN}Merging with QuizWhiz backup...{Colors.ENDC}")
        success, message = merge_quizwhiz_files(backup_file, current_file, final_output, append_mode, verbose=True)
        
        if not success:
            print(f"{Colors.FAIL}QuizWhiz merge failed: {message}{Colors.ENDC}")
            return
        
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        current_file = final_output
    
    # Final summary
    print(f"\n{Colors.HEADER}Workflow Complete!{Colors.ENDC}")
    print("=" * 50)
    print(f"{Colors.OKGREEN}🎉 All operations completed successfully!{Colors.ENDC}")
    print(f"Final output file: {Colors.BOLD}{current_file}{Colors.ENDC}")
    
    # Show file info
    try:
        with open(current_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'quizwhiz_quizzes' in data:
            total_questions = len(data['quizwhiz_quizzes'])
            print(f"Total questions: {Colors.BOLD}{total_questions}{Colors.ENDC}")
            
            # Calculate and display difficulty statistics
            difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
            for quiz_item in data['quizwhiz_quizzes']:
                difficulty = quiz_item.get("difficulty", "easy")
                if difficulty in difficulty_stats:
                    difficulty_stats[difficulty] += 1
            
            print(f"Difficulty breakdown:")
            print(f"  Easy: {Colors.OKGREEN}{difficulty_stats['easy']}{Colors.ENDC} questions")
            print(f"  Medium: {Colors.WARNING}{difficulty_stats['medium']}{Colors.ENDC} questions")
            print(f"  Hard: {Colors.FAIL}{difficulty_stats['hard']}{Colors.ENDC} questions")
            
        print(f"File size: {Colors.BOLD}{os.path.getsize(current_file) / 1024:.1f} KB{Colors.ENDC}")
    except:
        pass

def json_transformer_workflow():
    """JSON transformer workflow"""
    print(f"\n{Colors.HEADER}JSON Transformer Workflow{Colors.ENDC}")
    print("Transform existing JSON structures and apply NLP difficulty classification.\n")
    
    # Step 1: Source file selection
    print(f"{Colors.HEADER}Step 1: Source JSON File Selection{Colors.ENDC}")
    print("=" * 50)
    
    while True:
        source_file = input(f"{Colors.OKBLUE}Enter the path to your source JSON file: {Colors.ENDC}").strip()
        if not source_file:
            print(f"{Colors.WARNING}Please enter a valid file path.{Colors.ENDC}")
            continue
        
        source_file = os.path.expanduser(source_file)
        source_file = os.path.abspath(source_file)
        
        is_valid, error_msg = validate_json_file(source_file, "Source JSON")
        if not is_valid:
            print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
            continue
        
        break
    
    # Step 2: Optional QuizWhiz backup integration
    print(f"\n{Colors.HEADER}Step 2: QuizWhiz Backup Integration (Optional){Colors.ENDC}")
    print("=" * 50)
    
    backup_file = None
    append_mode = False
    
    while True:
        integrate_backup = input(f"{Colors.OKBLUE}Do you want to integrate with a QuizWhiz backup file? (y/n): {Colors.ENDC}").strip().lower()
        if integrate_backup in ['y', 'yes', 'n', 'no']:
            break
        print(f"{Colors.WARNING}Please enter 'y' or 'n'.{Colors.ENDC}")
    
    if integrate_backup in ['y', 'yes']:
        while True:
            backup_file = input(f"{Colors.OKBLUE}Enter the path to your QuizWhiz backup JSON file: {Colors.ENDC}").strip()
            if not backup_file:
                print(f"{Colors.WARNING}Please enter a valid file path.{Colors.ENDC}")
                continue
            
            backup_file = os.path.expanduser(backup_file)
            backup_file = os.path.abspath(backup_file)
            
            is_valid, error_msg = validate_json_file(backup_file, "QuizWhiz backup")
            if not is_valid:
                print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
                continue
            
            break
        
        # Ask for integration mode
        print(f"\n{Colors.OKBLUE}Integration mode options:{Colors.ENDC}")
        print("1. Replace - Replace all existing quizzes with transformed ones")
        print("2. Append - Add transformed quizzes to existing ones")
        
        while True:
            choice = input(f"{Colors.OKBLUE}Choose integration mode (1 or 2): {Colors.ENDC}").strip()
            if choice in ['1', '2']:
                append_mode = choice == '2'
                break
            print(f"{Colors.WARNING}Please enter 1 or 2.{Colors.ENDC}")
    
    # Step 3: NLP options
    print(f"\n{Colors.HEADER}Step 3: NLP Configuration{Colors.ENDC}")
    print("=" * 50)
    
    while True:
        apply_nlp = input(f"{Colors.OKBLUE}Apply NLP difficulty classification? (y/n): {Colors.ENDC}").strip().lower()
        if apply_nlp in ['y', 'yes', 'n', 'no']:
            apply_nlp = apply_nlp in ['y', 'yes']
            break
        print(f"{Colors.WARNING}Please enter 'y' or 'n'.{Colors.ENDC}")
    
    # Generate output filename
    source_path = Path(source_file)
    if backup_file:
        backup_path = Path(backup_file)
        output_file = str(backup_path.parent / f"{backup_path.stem}_TRANSFORMED.json")
    else:
        output_file = str(source_path.parent / f"{source_path.stem}_transformed.json")
    
    # Step 4: Transformation
    print(f"\n{Colors.HEADER}Step 4: JSON Transformation{Colors.ENDC}")
    print("=" * 50)
    
    print(f"\n{Colors.OKCYAN}Transforming JSON structure...{Colors.ENDC}")
    success, message = transform_json_structure(
        source_file, 
        output_file, 
        backup_file=backup_file,
        append_mode=append_mode,
        apply_nlp=apply_nlp,
        verbose=True
    )
    
    if not success:
        print(f"{Colors.FAIL}Transformation failed: {message}{Colors.ENDC}")
        return
    
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
    
    # Final summary
    print(f"\n{Colors.HEADER}Transformation Complete!{Colors.ENDC}")
    print("=" * 50)
    print(f"{Colors.OKGREEN}🎉 JSON transformation completed successfully!{Colors.ENDC}")
    print(f"Output file: {Colors.BOLD}{output_file}{Colors.ENDC}")
    
    # Show file info
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'quizwhiz_quizzes' in data:
            total_questions = len(data['quizwhiz_quizzes'])
            print(f"Total questions: {Colors.BOLD}{total_questions}{Colors.ENDC}")
            
            if apply_nlp:
                # Calculate and display difficulty statistics
                difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
                for quiz_item in data['quizwhiz_quizzes']:
                    difficulty = quiz_item.get("difficulty", "easy")
                    if difficulty in difficulty_stats:
                        difficulty_stats[difficulty] += 1
                
                print(f"Difficulty breakdown:")
                print(f"  Easy: {Colors.OKGREEN}{difficulty_stats['easy']}{Colors.ENDC} questions")
                print(f"  Medium: {Colors.WARNING}{difficulty_stats['medium']}{Colors.ENDC} questions")
                print(f"  Hard: {Colors.FAIL}{difficulty_stats['hard']}{Colors.ENDC} questions")
            
        print(f"File size: {Colors.BOLD}{os.path.getsize(output_file) / 1024:.1f} KB{Colors.ENDC}")
    except:
        pass

# ============================================================================
# GUI INTERFACE
# ============================================================================

class QuizToolkitGUI:
    def _windows_fluent_overhaul(self):
        """Rewrite visual style for Windows using flat sections instead of classic LabelFrames."""
        if self.system != "Windows":
            return
        # Force clam theme and rebuild styles for a flat, dark UI
        self.style.theme_use('clam')
        bg = self.colors['bg']; fg = self.colors['fg']
        frame_bg = self.colors.get('frame_bg', bg)
        entry_bg = self.colors.get('entry_bg', frame_bg)
        accent = self.colors.get('accent', fg)
        border = self.colors.get('border', frame_bg)
        # TFrame baseline
        self.style.configure('TFrame', background=bg)
        # Label baseline
        self.style.configure('TLabel', background=bg, foreground=fg)
        # Notebook
        self.style.configure('TNotebook', background=bg, borderwidth=0)
        self.style.configure('TNotebook.Tab', background=frame_bg, foreground=fg, padding=[12,6])
        self.style.map('TNotebook.Tab', background=[('selected', border), ('active', border)])
        # Buttons
        self.style.configure('TButton', background=frame_bg, foreground=fg, borderwidth=1, relief='solid')
        self.style.map('TButton', background=[('active', accent)])
        self.style.configure('Accent.TButton', background=accent, foreground=self.colors.get('button_fg', '#ffffff'), borderwidth=1, relief='solid')
        # Entries
        self.style.configure('TEntry', fieldbackground=entry_bg, foreground=fg, insertcolor=fg)
        # Progressbar
        self.style.configure('TProgressbar', background=accent, troughcolor=frame_bg)
        # Checkbutton/Radio
        self.style.configure('TCheckbutton', background=bg, foreground=fg)
        self.style.configure('TRadiobutton', background=bg, foreground=fg)
        # Kill LabelFrame chrome completely
        try:
            # Make default labelframe flat/transparent
            self.style.configure('TLabelframe', background=bg, borderwidth=0, relief='flat')
            self.style.configure('TLabelframe.Label', background=bg, foreground=fg)
            # Some themes use element names without T- prefix
            self.style.configure('Labelframe', background=bg, borderwidth=0, relief='flat')
            self.style.configure('Labelframe.Label', background=bg, foreground=fg)
            # Override layout to remove gradient/light fill
            for lf in ('TLabelframe','Labelframe'):
                try:
                    self.style.layout(lf, [('Labelframe.padding', {'sticky':'nswe','children':[('Labelframe.label', {'side':'top','sticky':'w'})]})])
                except Exception:
                    pass
        except Exception:
            pass
        # Walk all widgets: give scrolledtext/text, listboxes, and entries explicit dark props
        self._style_plain_tk_widgets(self.root)

    def __init__(self, root, force_light_mode=False):
        self.root = root
        self.force_light_mode = force_light_mode
        self.root.title("QuizWhiz JSON Toolkit - All-in-One QuizWhiz JSON Management Tool")
        self.root.geometry("900x900")
        self.root.minsize(800, 600)
        
        # Detect system and apply native styling
        self.setup_native_styling()
        
        # Apply theme based on system preference or force light mode
        self.setup_theme()
        
        # Create main container with native styling
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=self.padding, pady=self.padding)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True)
        self.notebook.bind('<<NotebookTabChanged>>', lambda e: self._style_plain_tk_widgets(self.root))

        
        # Create tabs
        self.create_extraction_tab()
        self.create_merger_tab()
        self.create_quizwhiz_tab()
        self.create_transformer_tab()
        
        # Status bar with integrated footer
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side='bottom', fill='x')
        
        # Status text on the left
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.status_frame, textvariable=self.status_var, relief='sunken')
        self.status_bar.pack(side='left', fill='x', expand=True)
        
        # Footer text on the right
        current_year = datetime.now().year
        footer_text = f"QuizWhiz JSON Toolkit v{VERSION} | (c) {current_year} RubyJ, made with 💗 for lablab"
        self.footer_label = ttk.Label(self.status_frame, text=footer_text, font=self.small_font)
        self.footer_label.pack(side='right', padx=10)
        
        # Set up theme refresh timer for Windows (to detect theme changes)
        # if self.system == "Windows":
        #     self.setup_theme_refresh()
        self._style_plain_tk_widgets(self.root)
        self.apply_dark_title_bar()

    
    def apply_dark_title_bar(self):
        """Use Windows DWM to enable an immersive dark title bar when in dark theme."""
        try:
            self.root.update_idletasks()
            if self.system == "Windows" and self.current_theme == 'dark':
                import ctypes
                import ctypes
                hwnd = self.root.winfo_id()
                # Some Windows builds require the parent hwnd for the title bar
                try:
                    hwnd = ctypes.windll.user32.GetParent(ctypes.c_void_p(hwnd)) or hwnd
                except Exception:
                    pass
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20  # works on Win10 1903+; falls back below
                value = ctypes.c_int(1)
                # Try attribute 20; if it fails, try 19 (older)
                res = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    ctypes.c_void_p(hwnd),
                    ctypes.c_uint(DWMWA_USE_IMMERSIVE_DARK_MODE),
                    ctypes.byref(value),
                    ctypes.sizeof(value)
                )
                if res != 0:
                    DWMWA_USE_IMMERSIVE_DARK_MODE = 19
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        ctypes.c_void_p(hwnd),
                        ctypes.c_uint(DWMWA_USE_IMMERSIVE_DARK_MODE),
                        ctypes.byref(value),
                        ctypes.sizeof(value)
                    )
        except Exception as e:
            # Non-fatal if it fails
            pass

    def _style_plain_tk_widgets(self, widget=None):
        """Force dark colors on classic Tk widgets that don't follow ttk styles, like Text and Scrollbar."""
        import tkinter as tk
        if widget is None:
            widget = self.root
        try:
            if isinstance(widget, tk.Text):
                try:
                    widget.configure(
                        bg=self.colors.get('text_bg', self.colors['frame_bg']),
                        fg=self.colors['fg'],
                        insertbackground=self.colors['fg'],
                        selectbackground=self.colors.get('select_bg', self.colors['accent']),
                        selectforeground=self.colors.get('select_fg', self.colors['button_fg']),
                        highlightbackground=self.colors.get('border', self.colors['frame_bg']),
                        highlightcolor=self.colors.get('accent', self.colors['fg'])
                    )
                except Exception:
                    pass
            elif isinstance(widget, tk.Entry):
                try:
                    widget.configure(
                        bg=self.colors.get('entry_bg', self.colors['frame_bg']),
                        fg=self.colors['fg'],
                        insertbackground=self.colors['fg'],
                        highlightbackground=self.colors.get('border', self.colors['frame_bg'])
                    )
                except Exception:
                    pass
            elif isinstance(widget, tk.Listbox):
                try:
                    widget.configure(
                        bg=self.colors.get('text_bg', self.colors['frame_bg']),
                        fg=self.colors['fg'],
                        selectbackground=self.colors.get('select_bg', self.colors['accent']),
                        selectforeground=self.colors.get('select_fg', self.colors['button_fg'])
                    )
                except Exception:
                    pass
            elif isinstance(widget, tk.Scrollbar):
                # Classic scrollbar doesn't take fg/bg the same; best effort via highlight
                try:
                    widget.configure(
                        troughcolor=self.colors.get('frame_bg', self.colors['bg']),
                        activebackground=self.colors.get('accent', self.colors['fg']),
                        highlightbackground=self.colors.get('border', self.colors['frame_bg'])
                    )
                except Exception:
                    pass
        except Exception:
            pass
        # Recurse into children
        for child in getattr(widget, "winfo_children", lambda: [])():
            self._style_plain_tk_widgets(child)

    def setup_native_styling(self):
        """Setup native styling based on the operating system"""
        self.system = platform.system()
        
        # Set platform-specific styling
        if self.system == "Darwin":  # macOS
            self.setup_macos_styling()
        elif self.system == "Windows":
            self.setup_windows_styling()
        else:  # Linux and others
            self.setup_linux_styling()
    
    def setup_macos_styling(self):
        """Apply macOS native design language"""
        # macOS specific styling
        self.padding = 20
        self.button_padding = (10, 8)
        self.frame_padding = 15
        
        # Configure ttk style for macOS
        self.style = ttk.Style()
        
        # Use aqua theme if available, otherwise default
        try:
            self.style.theme_use('aqua')
        except tk.TclError:
            self.style.theme_use('clam')
        
        # macOS specific fonts
        self.title_font = ('SF Pro Display', 16, 'bold')
        self.heading_font = ('SF Pro Display', 14, 'bold')
        self.body_font = ('SF Pro Text', 12)
        self.small_font = ('SF Pro Text', 11)
        
        # Configure window for macOS
        self.root.configure(bg='systemWindowBackgroundColor')
        
        # macOS window styling
        try:
            # Enable native window styling on macOS
            self.root.tk.call('::tk::unsupported::MacWindowStyle', 'style', self.root._w, 'document')
        except tk.TclError:
            pass
    
    def setup_windows_styling(self):
        """Apply Windows native design language (Fluent Design)"""
        self.padding = 16
        self.button_padding = (12, 6)
        self.frame_padding = 12
        
        self.style = ttk.Style()
        # Use default theme to allow better custom styling
        self.style.theme_use('clam')
        
        # Windows specific fonts
        self.title_font = ('Segoe UI', 16, 'bold')
        self.heading_font = ('Segoe UI', 14, 'bold')
        self.body_font = ('Segoe UI', 10)
        self.small_font = ('Segoe UI', 9)
    
    def setup_linux_styling(self):
        """Apply Linux/GTK styling"""
        self.padding = 12
        self.button_padding = (10, 6)
        self.frame_padding = 10
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Linux specific fonts
        self.title_font = ('Ubuntu', 16, 'bold')
        self.heading_font = ('Ubuntu', 14, 'bold')
        self.body_font = ('Ubuntu', 11)
        self.small_font = ('Ubuntu', 10)
    
    def detect_system_theme(self):
        """Detect system theme (light/dark mode)"""
        if self.system == "Darwin":  # macOS
            try:
                # Check macOS dark mode
                result = subprocess.run(
                    ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                    capture_output=True, text=True
                )
                return 'dark' if result.returncode == 0 and 'Dark' in result.stdout else 'light'
            except:
                return 'light'
        elif self.system == "Windows":
            try:
                # Check Windows dark mode
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                winreg.CloseKey(key)
                return 'light' if value else 'dark'
            except (OSError, FileNotFoundError, winreg.error):
                # Fallback: try to detect from system colors
                try:
                    import tkinter as tk
                    temp_root = tk.Tk()
                    temp_root.withdraw()
                    bg_color = temp_root.cget('bg')
                    temp_root.destroy()
                    # Simple heuristic: if background is dark, assume dark theme
                    return 'dark' if bg_color in ['#212121', '#2d2d30', '#1e1e1e'] else 'light'
                except:
                    return 'light'
        else:
            # Linux - try to detect from environment
            try:
                import os
                gtk_theme = os.environ.get('GTK_THEME', '')
                if 'dark' in gtk_theme.lower():
                    return 'dark'
                return 'light'
            except:
                return 'light'
    
    def setup_theme(self):
        """Setup theme based on system preference or force light mode"""
        if self.force_light_mode:
            self.current_theme = 'light'
        else:
            self.current_theme = self.detect_system_theme()
        
        if self.current_theme == 'dark':
            self.setup_dark_theme()
        else:
            self.setup_light_theme()
        # Apply dark title bar on Windows when in dark mode
        self.apply_dark_title_bar()
    

    def setup_light_theme(self):
        """Configure light theme colors and styles"""
        if self.system == "Darwin":  # macOS light theme
            self.colors = {
                'bg': '#ffffff',
                'fg': '#000000',
                'select_bg': '#007AFF',
                'select_fg': '#ffffff',
                'frame_bg': '#f5f5f5',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'button_bg': '#007AFF',
                'button_fg': '#ffffff',
                'accent': '#007AFF',
                'secondary': '#8E8E93',
                'success': '#34C759',
                'warning': '#FF9500',
                'error': '#FF3B30',
                'footer_fg': '#8E8E93',
                'text_bg': '#ffffff',
                'border': '#d1d1d6'
            }
        elif self.system == "Windows":  # Windows light theme (Fluent Design)
            self.colors = {
                'bg': '#ffffff',  # Pure white background
                'fg': '#323130',  # Fluent neutral foreground
                'select_bg': '#0078d4',
                'select_fg': '#ffffff',
                'frame_bg': '#faf9f8',  # Fluent card background
                'entry_bg': '#ffffff',
                'entry_fg': '#323130',
                'button_bg': '#0078d4',
                'button_fg': '#ffffff',
                'accent': '#0078d4',  # Windows accent blue
                'secondary': '#605e5c',  # Fluent neutral secondary
                'success': '#107c10',
                'warning': '#ff8c00',
                'error': '#d13438',
                'footer_fg': '#605e5c',
                'text_bg': '#ffffff',  # Specific for text widgets
                'border': '#d2d0ce'  # Fluent border color
            }
        else:  # Linux light theme
            self.colors = {
                'bg': '#ffffff',
                'fg': '#2e3436',
                'select_bg': '#3584e4',
                'select_fg': '#ffffff',
                'frame_bg': '#f6f5f4',
                'entry_bg': '#ffffff',
                'entry_fg': '#2e3436',
                'button_bg': '#3584e4',
                'button_fg': '#ffffff',
                'accent': '#3584e4',
                'secondary': '#9a9996',
                'success': '#26a269',
                'warning': '#f57c00',
                'error': '#e01b24',
                'footer_fg': '#9a9996',
                'text_bg': '#ffffff',
                'border': '#c0bfbc'
            }
        
        self.apply_theme_styles()
    
    def setup_dark_theme(self):
        """Configure dark theme colors and styles"""
        if self.system == "Darwin":  # macOS dark theme
            self.colors = {
                'bg': '#1e1e1e',
                'fg': '#ffffff',
                'select_bg': '#0A84FF',
                'select_fg': '#ffffff',
                'frame_bg': '#2d2d2d',
                'entry_bg': '#3a3a3a',
                'entry_fg': '#ffffff',
                'button_bg': '#0A84FF',
                'button_fg': '#ffffff',
                'accent': '#0A84FF',
                'secondary': '#98989D',
                'success': '#30D158',
                'warning': '#FF9F0A',
                'error': '#FF453A',
                'footer_fg': '#98989D',
                'text_bg': '#2d2d2d',
                'border': '#48484a'
            }
        elif self.system == "Windows":  # Windows dark theme (Fluent Design)
            self.colors = {
                'bg': '#1e1e1e',  # Modern Windows dark background
                'fg': '#ffffff',
                'select_bg': '#0078d4',
                'select_fg': '#ffffff',
                'frame_bg': '#2d2d30',  # Fluent card background
                'entry_bg': '#323130',  # Fluent input background
                'entry_fg': '#ffffff',
                'button_bg': '#0078d4',
                'button_fg': '#ffffff',
                'accent': '#0078d4',  # Windows accent blue
                'secondary': '#8a8886',  # Fluent neutral foreground
                'success': '#107c10',
                'warning': '#ff8c00',
                'error': '#d13438',
                'footer_fg': '#8a8886',  # Fluent subtle text
                'text_bg': '#323130',  # Specific for text widgets
                'border': '#605e5c'  # Fluent border color
            }
        else:  # Linux dark theme
            self.colors = {
                'bg': '#242424',
                'fg': '#ffffff',
                'select_bg': '#3584e4',
                'select_fg': '#ffffff',
                'frame_bg': '#303030',
                'entry_bg': '#3a3a3a',
                'entry_fg': '#ffffff',
                'button_bg': '#3584e4',
                'button_fg': '#ffffff',
                'accent': '#3584e4',
                'secondary': '#9a9996',
                'success': '#26a269',
                'warning': '#f57c00',
                'error': '#e01b24',
                'footer_fg': '#9a9996',
                'text_bg': '#2d2d2d',
                'border': '#555753'
            }
        
        self.apply_theme_styles()
    
    def apply_theme_styles(self):
        """Apply the current theme to all UI elements"""
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        # Windows visual overhaul for a flat, modern dark UI
        self._windows_fluent_overhaul()
        
        # Configure ttk styles
        border_color = self.colors.get('border', self.colors['secondary'])
        
        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        self.style.configure('TLabelFrame', 
                           background=self.colors['bg'], 
                           foreground=self.colors['fg'],
                           bordercolor=border_color,
                           lightcolor=self.colors['frame_bg'],
                           darkcolor=self.colors['frame_bg'],
                           relief='solid',
                           borderwidth=1)
        self.style.configure('TLabelFrame.Label', 
                           background=self.colors['bg'], 
                           foreground=self.colors['fg'])
        
        # Entry styling with modern borders
        self.style.configure('TEntry', 
                           fieldbackground=self.colors['entry_bg'],
                           foreground=self.colors['entry_fg'],
                           bordercolor=border_color,
                           lightcolor=self.colors['frame_bg'],
                           darkcolor=self.colors['frame_bg'],
                           relief='solid',
                           borderwidth=1,
                           focuscolor=self.colors['accent'],
                           selectbackground=self.colors['accent'],
                           selectforeground=self.colors['bg'])
        
        self.style.map('TEntry',
                      fieldbackground=[('focus', self.colors['entry_bg']),
                                     ('active', self.colors['entry_bg'])],
                      bordercolor=[('focus', self.colors['accent']),
                                 ('active', self.colors['accent'])])
        
        # Button styling with modern Fluent Design
        self.style.configure('TButton',
                           background=self.colors['button_bg'],
                           foreground=self.colors['button_fg'],
                           bordercolor=self.colors['button_bg'],
                           focuscolor='none',
                           relief='solid',
                           borderwidth=1,
                           padding=[12, 8])
        
        self.style.map('TButton',
                      background=[('active', self.colors['accent']),
                                ('pressed', self.colors['secondary']),
                                ('disabled', self.colors['frame_bg'])],
                      foreground=[('disabled', self.colors['secondary'])])
        
        # Accent button style with enhanced appearance
        self.style.configure('Accent.TButton',
                           background=self.colors['accent'],
                           foreground=self.colors['button_fg'],
                           bordercolor=self.colors['accent'],
                           relief='solid',
                           borderwidth=1,
                           padding=[12, 8])
        
        # Notebook styling
        self.style.configure('TNotebook', background=self.colors['bg'])
        self.style.configure('TNotebook.Tab',
                           background=self.colors['frame_bg'],
                           foreground=self.colors['fg'],
                           padding=[12, 8])
        
        self.style.map('TNotebook.Tab',
                      background=[('selected', self.colors['bg']),
                                ('active', self.colors['select_bg'])],
                      foreground=[('selected', self.colors['fg']),
                                ('active', self.colors['select_fg'])])
        
        # Checkbutton styling for dark mode
        self.style.configure('TCheckbutton',
                           background=self.colors['bg'],
                           foreground=self.colors['fg'],
                           focuscolor='none',
                           indicatorbackground=self.colors['entry_bg'],
                           indicatorforeground=self.colors['fg'])
        
        self.style.map('TCheckbutton',
                      background=[('active', self.colors['bg']),
                                ('pressed', self.colors['frame_bg'])],
                      indicatorcolor=[('selected', self.colors['accent']),
                                    ('!selected', self.colors['entry_bg'])])
        
        # Radiobutton styling for dark mode
        self.style.configure('TRadiobutton',
                           background=self.colors['bg'],
                           foreground=self.colors['fg'],
                           focuscolor='none',
                           indicatorbackground=self.colors['entry_bg'],
                           indicatorforeground=self.colors['fg'])
        
        self.style.map('TRadiobutton',
                      background=[('active', self.colors['bg']),
                                ('pressed', self.colors['frame_bg'])],
                      indicatorcolor=[('selected', self.colors['accent']),
                                    ('!selected', self.colors['entry_bg'])])
        
        # Combobox styling for dark mode
        self.style.configure('TCombobox',
                           fieldbackground=self.colors['entry_bg'],
                           background=self.colors['entry_bg'],
                           foreground=self.colors['entry_fg'],
                           bordercolor=border_color,
                           lightcolor=self.colors['frame_bg'],
                           darkcolor=self.colors['frame_bg'],
                           arrowcolor=self.colors['fg'],
                           insertcolor=self.colors['entry_fg'])
        
        self.style.map('TCombobox',
                      fieldbackground=[('readonly', self.colors['entry_bg']),
                                     ('disabled', self.colors['frame_bg'])],
                      foreground=[('disabled', self.colors['secondary'])])
        
        # Configure combobox dropdown
        self.root.option_add('*TCombobox*Listbox*Background', self.colors['entry_bg'])
        self.root.option_add('*TCombobox*Listbox*Foreground', self.colors['entry_fg'])
        self.root.option_add('*TCombobox*Listbox*selectBackground', self.colors['select_bg'])
        self.root.option_add('*TCombobox*Listbox*selectForeground', self.colors['select_fg'])
        
        # Progressbar styling
        self.style.configure('TProgressbar',
                           background=self.colors['accent'],
                           troughcolor=self.colors['frame_bg'],
                           bordercolor=self.colors['secondary'],
                           lightcolor=self.colors['accent'],
                           darkcolor=self.colors['accent'])
        
        # Scrollbar styling
        self.style.configure('Vertical.TScrollbar',
                           background=self.colors['frame_bg'],
                           troughcolor=self.colors['bg'],
                           bordercolor=self.colors['secondary'],
                           arrowcolor=self.colors['fg'],
                           darkcolor=self.colors['frame_bg'],
                           lightcolor=self.colors['frame_bg'])
        
        # Update footer label color if it exists
        if hasattr(self, 'footer_label'):
            self.footer_label.configure(foreground=self.colors['footer_fg'])
        
        # Update scrolledtext widgets if they exist
        text_widgets = ['results_text', 'merge_results_text', 'qw_results_text', 'transform_results_text']
        for widget_name in text_widgets:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                # Use specific text background color for better contrast
                text_bg = self.colors.get('text_bg', self.colors['entry_bg'])
                border_color = self.colors.get('border', self.colors['secondary'])
                
                widget.configure(
                    bg=text_bg,
                    fg=self.colors['entry_fg'],
                    insertbackground=self.colors['entry_fg'],
                    selectbackground=self.colors['select_bg'],
                    selectforeground=self.colors['select_fg'],
                    relief='solid',
                    borderwidth=1,
                    highlightthickness=0
                )
                
                # Configure the internal text widget for better styling
                try:
                    text_widget = widget.text if hasattr(widget, 'text') else widget
                    text_widget.configure(
                        bg=text_bg,
                        fg=self.colors['entry_fg'],
                        insertbackground=self.colors['entry_fg'],
                        selectbackground=self.colors['select_bg'],
                        selectforeground=self.colors['select_fg']
                    )
                except:
                    pass  # Fallback if text widget access fails
        
        # Update tk.Listbox widgets if they exist
        listbox_widgets = ['file_listbox']
        for widget_name in listbox_widgets:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                text_bg = self.colors.get('text_bg', self.colors['entry_bg'])
                border_color = self.colors.get('border', self.colors['secondary'])
                
                widget.configure(
                    bg=text_bg,
                    fg=self.colors['entry_fg'],
                    selectbackground=self.colors['select_bg'],
                    selectforeground=self.colors['select_fg'],
                    highlightbackground=border_color,
                    highlightcolor=self.colors['accent'],
                    highlightthickness=1,
                    relief='solid',
                    borderwidth=1
                )
        # Also force dark styling on classic Tk widgets (Text, Listbox, Scrollbar)
        self._style_plain_tk_widgets(self.root)
    

    def setup_theme_refresh(self):
        """Setup automatic theme refresh for Windows to detect system theme changes"""
        if self.system == "Windows":
            # Check for theme changes every 5 seconds
            self.root.after(5000, self.check_theme_change)
    
    def check_theme_change(self):
        """Check if Windows theme has changed and refresh if needed"""
        if self.system == "Windows":
            new_theme = self.detect_system_theme()
            if new_theme != self.current_theme:
                self.current_theme = new_theme
                self.refresh_theme()
            # Schedule next check
            self.root.after(5000, self.check_theme_change)
    
    def refresh_theme(self):
        """Refresh the current theme without recreating the entire UI"""
        if self.current_theme == 'dark':
            self.setup_dark_theme()
        else:
            self.setup_light_theme()
        
        # Force update all widgets
        self.root.update_idletasks()
        # Re-style classic Tk widgets
        self._style_plain_tk_widgets(self.root)
        
        # Trigger a redraw of all widgets
        def update_widget_tree(widget):
            try:
                if hasattr(widget, 'configure'):
                    widget.update()
                for child in widget.winfo_children():
                    update_widget_tree(child)
            except:
                pass
        
        update_widget_tree(self.root)
    
    def create_extraction_tab(self):
        """Create the MHTML extraction tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Google Form MHTML Extraction")
        
        # Main frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Extract Quiz Data from Google Forms MHTML Files", 
                               font=self.heading_font)
        title_label.pack(pady=(0, self.padding))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=self.frame_padding)
        file_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        ttk.Label(file_frame, text="MHTML File:").pack(anchor='w')
        file_input_frame = ttk.Frame(file_frame)
        file_input_frame.pack(fill='x', pady=(5, 10))
        
        self.mhtml_file_var = tk.StringVar()
        self.mhtml_entry = ttk.Entry(file_input_frame, textvariable=self.mhtml_file_var, width=60)
        self.mhtml_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(file_input_frame, text="Browse", 
                  command=self.browse_mhtml_file).pack(side='right', padx=(5, 0))
        
        # Deck name
        ttk.Label(file_frame, text="Deck Name:").pack(anchor='w')
        self.deck_name_var = tk.StringVar()
        self.deck_entry = ttk.Entry(file_frame, textvariable=self.deck_name_var, width=60)
        self.deck_entry.pack(fill='x', pady=(5, 10))
        
        # Output file
        ttk.Label(file_frame, text="Output File (optional):").pack(anchor='w')
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill='x', pady=(5, 0))
        
        self.output_file_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var, width=60)
        self.output_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_output_file).pack(side='right', padx=(5, 0))
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=self.frame_padding)
        options_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        self.verbose_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Verbose output", 
                       variable=self.verbose_var).pack(anchor='w')
        
        # Progress
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=self.frame_padding)
        progress_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        self.progress_var = tk.StringVar()
        self.progress_var.set("Ready to extract...")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(anchor='w')
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill='x', pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(self.frame_padding, 0))
        
        ttk.Button(button_frame, text="Extract Quiz Data", 
                  command=self.extract_quiz, style='Accent.TButton').pack(side='left')
        
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_extraction_form).pack(side='left', padx=(10, 0))
        
        # Results
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=self.frame_padding)
        results_frame.pack(fill='both', expand=True, pady=(self.frame_padding, 0))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=8, wrap='word')
        self.results_text.pack(fill='both', expand=True)
    
    def create_merger_tab(self):
        """Create the JSON merger tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="JSON Output Merger")
        
        # Main frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Merge Multiple Quiz JSON Files", 
                               font=self.heading_font)
        title_label.pack(pady=(0, self.padding))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=self.frame_padding)
        file_frame.pack(fill='both', expand=True, pady=(0, self.frame_padding))
        
        # File list
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill='both', expand=True)
        
        ttk.Label(list_frame, text="Files to merge:").pack(anchor='w')
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill='both', expand=True, pady=(5, 10))
        
        self.file_listbox = tk.Listbox(listbox_frame, height=8)
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # File buttons
        file_button_frame = ttk.Frame(list_frame)
        file_button_frame.pack(fill='x')
        
        ttk.Button(file_button_frame, text="Add Files", 
                  command=self.add_merge_files).pack(side='left')
        ttk.Button(file_button_frame, text="Remove Selected", 
                  command=self.remove_merge_file).pack(side='left', padx=(5, 0))
        ttk.Button(file_button_frame, text="Clear All", 
                  command=self.clear_merge_files).pack(side='left', padx=(5, 0))
        
        # Output file
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Label(output_frame, text="Output File (optional):").pack(anchor='w')
        output_input_frame = ttk.Frame(output_frame)
        output_input_frame.pack(fill='x', pady=(5, 0))
        
        self.merge_output_var = tk.StringVar()
        self.merge_output_entry = ttk.Entry(output_input_frame, textvariable=self.merge_output_var)
        self.merge_output_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(output_input_frame, text="Browse", 
                  command=self.browse_merge_output).pack(side='right', padx=(5, 0))
        
        # Progress
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=self.frame_padding)
        progress_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        self.merge_progress_var = tk.StringVar()
        self.merge_progress_var.set("Ready to merge...")
        ttk.Label(progress_frame, textvariable=self.merge_progress_var).pack(anchor='w')
        
        self.merge_progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.merge_progress_bar.pack(fill='x', pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="Merge Files", 
                  command=self.merge_files, style='Accent.TButton').pack(side='left')
        
        # Results
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=self.frame_padding)
        results_frame.pack(fill='x', pady=(self.frame_padding, 0))
        
        self.merge_results_text = scrolledtext.ScrolledText(results_frame, height=4, wrap='word')
        self.merge_results_text.pack(fill='both', expand=True)
    
    def create_quizwhiz_tab(self):
        """Create the QuizWhiz backup merger tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="QuizWhiz JSON Backup Merger")
        
        # Main frame
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Merge Quiz Data with QuizWhiz Backup", 
                               font=self.heading_font)
        title_label.pack(pady=(0, self.padding))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=self.frame_padding)
        file_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        # Backup file
        ttk.Label(file_frame, text="QuizWhiz Backup File:").pack(anchor='w')
        backup_input_frame = ttk.Frame(file_frame)
        backup_input_frame.pack(fill='x', pady=(5, 10))
        
        self.backup_file_var = tk.StringVar()
        self.backup_entry = ttk.Entry(backup_input_frame, textvariable=self.backup_file_var)
        self.backup_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(backup_input_frame, text="Browse", 
                  command=self.browse_backup_file).pack(side='right', padx=(5, 0))
        
        # Quiz file
        ttk.Label(file_frame, text="Quiz JSON File:").pack(anchor='w')
        quiz_input_frame = ttk.Frame(file_frame)
        quiz_input_frame.pack(fill='x', pady=(5, 10))
        
        self.quiz_file_var = tk.StringVar()
        self.quiz_entry = ttk.Entry(quiz_input_frame, textvariable=self.quiz_file_var)
        self.quiz_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(quiz_input_frame, text="Browse", 
                  command=self.browse_quiz_file).pack(side='right', padx=(5, 0))
        
        # Output file
        ttk.Label(file_frame, text="Output File (optional):").pack(anchor='w')
        qw_output_frame = ttk.Frame(file_frame)
        qw_output_frame.pack(fill='x', pady=(5, 0))
        
        self.qw_output_var = tk.StringVar()
        self.qw_output_entry = ttk.Entry(qw_output_frame, textvariable=self.qw_output_var)
        self.qw_output_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(qw_output_frame, text="Browse", 
                  command=self.browse_qw_output).pack(side='right', padx=(5, 0))
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Merge Options", padding=self.frame_padding)
        options_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        self.merge_mode_var = tk.StringVar(value="replace")
        ttk.Radiobutton(options_frame, text="Replace existing quizzes", 
                       variable=self.merge_mode_var, value="replace").pack(anchor='w')
        ttk.Radiobutton(options_frame, text="Append to existing quizzes", 
                       variable=self.merge_mode_var, value="append").pack(anchor='w')
        
        self.qw_verbose_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Verbose output", 
                       variable=self.qw_verbose_var).pack(anchor='w', pady=(5, 0))
        
        # Progress
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=self.frame_padding)
        progress_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        self.qw_progress_var = tk.StringVar()
        self.qw_progress_var.set("Ready to merge...")
        ttk.Label(progress_frame, textvariable=self.qw_progress_var).pack(anchor='w')
        
        self.qw_progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.qw_progress_bar.pack(fill='x', pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="Merge with QuizWhiz", 
                  command=self.merge_quizwhiz, style='Accent.TButton').pack(side='left')
        
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_quizwhiz_form).pack(side='left', padx=(self.frame_padding, 0))
        
        # Results
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=self.frame_padding)
        results_frame.pack(fill='both', expand=True, pady=(self.frame_padding, 0))
        
        self.qw_results_text = scrolledtext.ScrolledText(results_frame, height=6, wrap='word')
        self.qw_results_text.pack(fill='both', expand=True)
    
    def create_transformer_tab(self):
        """Create the JSON Transformer tab"""
        transformer_frame = ttk.Frame(self.notebook)
        self.notebook.add(transformer_frame, text="JSON Transformer")
        
        # Main container with padding
        main_frame = ttk.Frame(transformer_frame)
        main_frame.pack(fill='both', expand=True, padx=self.padding, pady=self.padding)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding=self.frame_padding)
        file_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        # Source JSON file
        ttk.Label(file_frame, text="Source JSON File:").pack(anchor='w')
        source_frame = ttk.Frame(file_frame)
        source_frame.pack(fill='x', pady=(5, 10))
        
        self.transform_source_var = tk.StringVar()
        self.transform_source_entry = ttk.Entry(source_frame, textvariable=self.transform_source_var, width=60)
        self.transform_source_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(source_frame, text="Browse", 
                  command=self.browse_transform_source).pack(side='right', padx=(5, 0))
        
        # QuizWhiz backup file (optional)
        ttk.Label(file_frame, text="QuizWhiz Backup File (optional):").pack(anchor='w')
        backup_frame = ttk.Frame(file_frame)
        backup_frame.pack(fill='x', pady=(5, 10))
        
        self.transform_backup_var = tk.StringVar()
        self.transform_backup_entry = ttk.Entry(backup_frame, textvariable=self.transform_backup_var, width=60)
        self.transform_backup_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(backup_frame, text="Browse", 
                  command=self.browse_transform_backup).pack(side='right', padx=(5, 0))
        
        # Output file
        ttk.Label(file_frame, text="Output File:").pack(anchor='w')
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill='x', pady=(5, 0))
        
        self.transform_output_var = tk.StringVar()
        self.transform_output_entry = ttk.Entry(output_frame, textvariable=self.transform_output_var, width=60)
        self.transform_output_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_transform_output).pack(side='right', padx=(5, 0))
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=self.frame_padding)
        options_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        # Merge mode for backup integration
        ttk.Label(options_frame, text="Backup Integration Mode:").pack(anchor='w')
        self.transform_mode_var = tk.StringVar(value="replace")
        mode_frame = ttk.Frame(options_frame)
        mode_frame.pack(fill='x', pady=(5, 10))
        
        ttk.Radiobutton(mode_frame, text="Replace existing quizzes", 
                       variable=self.transform_mode_var, value="replace").pack(anchor='w')
        ttk.Radiobutton(mode_frame, text="Append to existing quizzes", 
                       variable=self.transform_mode_var, value="append").pack(anchor='w')
        
        self.transform_verbose_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Verbose output", 
                       variable=self.transform_verbose_var).pack(anchor='w', pady=(5, 0))
        
        self.transform_apply_nlp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Apply NLP difficulty classification", 
                       variable=self.transform_apply_nlp_var).pack(anchor='w', pady=(5, 0))
        
        # Progress
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=self.frame_padding)
        progress_frame.pack(fill='x', pady=(0, self.frame_padding))
        
        self.transform_progress_var = tk.StringVar()
        self.transform_progress_var.set("Ready to transform...")
        ttk.Label(progress_frame, textvariable=self.transform_progress_var).pack(anchor='w')
        
        self.transform_progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.transform_progress_bar.pack(fill='x', pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="Transform JSON", 
                  command=self.transform_json, style='Accent.TButton').pack(side='left')
        
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_transform_form).pack(side='left', padx=(self.frame_padding, 0))
        
        # Results
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=self.frame_padding)
        results_frame.pack(fill='both', expand=True, pady=(self.frame_padding, 0))
        
        self.transform_results_text = scrolledtext.ScrolledText(results_frame, height=6, wrap='word')
        self.transform_results_text.pack(fill='both', expand=True)
    
    # Event handlers for extraction tab
    def browse_mhtml_file(self):
        filename = filedialog.askopenfilename(
            title="Select MHTML File",
            filetypes=[("MHTML files", "*.mhtml"), ("All files", "*.*")]
        )
        if filename:
            self.mhtml_file_var.set(filename)
            # Auto-generate deck name from filename (always update)
            base_name = os.path.splitext(os.path.basename(filename))[0]
            clean_name = re.sub(r'[<>:"/\\|?*]', '_', base_name)
            self.deck_name_var.set(clean_name)
    
    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save Extracted Quiz As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
    
    def clear_extraction_form(self):
        self.mhtml_file_var.set("")
        self.deck_name_var.set("")
        self.output_file_var.set("")
        self.verbose_var.set(False)
        self.results_text.delete(1.0, tk.END)
        self.progress_var.set("Ready to extract...")
    
    def extract_quiz(self):
        if not self.mhtml_file_var.get():
            messagebox.showerror("Error", "Please select an MHTML file.")
            return
        
        if not self.deck_name_var.get():
            messagebox.showerror("Error", "Please enter a deck name.")
            return
        
        # Generate output filename if not provided
        output_file = self.output_file_var.get()
        if not output_file:
            safe_name = re.sub(r'[<>:"/\\|?*]', '_', self.deck_name_var.get())
            output_file = f"{safe_name.lower().replace(' ', '_')}.json"
        
        # Run extraction in a separate thread
        def run_extraction():
            self.progress_bar.start()
            self.progress_var.set("Starting extraction...")
            self.results_text.delete(1.0, tk.END)
            
            def progress_callback(message):
                self.root.after(0, lambda: self.progress_var.set(message))
            
            try:
                result, message = extract_quiz_from_mhtml(
                    self.mhtml_file_var.get(),
                    self.deck_name_var.get(),
                    output_file,
                    verbose=self.verbose_var.get(),
                    progress_callback=progress_callback
                )
                
                self.root.after(0, lambda: self.extraction_complete(result, message, output_file))
            except Exception as e:
                self.root.after(0, lambda: self.extraction_error(str(e)))
        
        threading.Thread(target=run_extraction, daemon=True).start()
    
    def extraction_complete(self, result, message, output_file):
        self.progress_bar.stop()
        if result is None:
            self.progress_var.set("Extraction failed")
            self.results_text.insert(tk.END, f"Error: {message}\n")
            messagebox.showerror("Extraction Failed", message)
        else:
            self.progress_var.set("Extraction completed successfully")
            self.results_text.insert(tk.END, f"Success: {message}\n")
            self.results_text.insert(tk.END, f"Output file: {output_file}\n")
            self.results_text.insert(tk.END, f"Questions extracted: {len(result['quizwhiz_quizzes'])}\n")
            
            # Calculate and display difficulty statistics
            difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
            for quiz_item in result['quizwhiz_quizzes']:
                difficulty = quiz_item.get("difficulty", "easy")
                if difficulty in difficulty_stats:
                    difficulty_stats[difficulty] += 1
            
            self.results_text.insert(tk.END, f"\nDifficulty Distribution:\n")
            self.results_text.insert(tk.END, f"  Easy: {difficulty_stats['easy']} questions\n")
            self.results_text.insert(tk.END, f"  Medium: {difficulty_stats['medium']} questions\n")
            self.results_text.insert(tk.END, f"  Hard: {difficulty_stats['hard']} questions\n")
            
            messagebox.showinfo("Success", f"Extraction completed!\n{message}")
    
    def extraction_error(self, error_msg):
        self.progress_bar.stop()
        self.progress_var.set("Extraction failed")
        self.results_text.insert(tk.END, f"Error: {error_msg}\n")
        messagebox.showerror("Error", f"Extraction failed: {error_msg}")
    
    # Event handlers for merger tab
    def add_merge_files(self):
        filenames = filedialog.askopenfilenames(
            title="Select Quiz JSON Files",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        for filename in filenames:
            if filename not in self.file_listbox.get(0, tk.END):
                self.file_listbox.insert(tk.END, filename)
    
    def remove_merge_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            self.file_listbox.delete(selection[0])
    
    def clear_merge_files(self):
        self.file_listbox.delete(0, tk.END)
        self.merge_output_var.set("")
        self.merge_results_text.delete(1.0, tk.END)
    
    def browse_merge_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Merged Quiz As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.merge_output_var.set(filename)
    
    def merge_files(self):
        files = list(self.file_listbox.get(0, tk.END))
        if len(files) < 2:
            messagebox.showerror("Error", "Please select at least 2 files to merge.")
            return
        
        output_file = self.merge_output_var.get()
        
        def run_merge():
            self.merge_progress_bar.start()
            self.merge_progress_var.set("Starting merge...")
            self.merge_results_text.delete(1.0, tk.END)
            
            def progress_callback(message):
                self.root.after(0, lambda: self.merge_progress_var.set(message))
            
            try:
                result_file, message = merge_quiz_files(
                    files, output_file, verbose=True, progress_callback=progress_callback
                )
                
                self.root.after(0, lambda: self.merge_complete(result_file, message))
            except Exception as e:
                self.root.after(0, lambda: self.merge_error(str(e)))
        
        threading.Thread(target=run_merge, daemon=True).start()
    
    def merge_complete(self, result_file, message):
        self.merge_progress_bar.stop()
        if result_file is None:
            self.merge_progress_var.set("Merge failed")
            self.merge_results_text.insert(tk.END, f"Error: {message}\n")
            messagebox.showerror("Merge Failed", message)
        else:
            self.merge_progress_var.set("Merge completed successfully")
            self.merge_results_text.insert(tk.END, f"Success: {message}\n")
            self.merge_results_text.insert(tk.END, f"Output file: {result_file}\n")
            messagebox.showinfo("Success", f"Merge completed!\n{message}")
    
    def merge_error(self, error_msg):
        self.merge_progress_bar.stop()
        self.merge_progress_var.set("Merge failed")
        self.merge_results_text.insert(tk.END, f"Error: {error_msg}\n")
        messagebox.showerror("Error", f"Merge failed: {error_msg}")
    
    # Event handlers for QuizWhiz tab
    def browse_backup_file(self):
        filename = filedialog.askopenfilename(
            title="Select QuizWhiz Backup File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.backup_file_var.set(filename)
    
    def browse_quiz_file(self):
        filename = filedialog.askopenfilename(
            title="Select Quiz JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.quiz_file_var.set(filename)
    
    def browse_qw_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Merged QuizWhiz File As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.qw_output_var.set(filename)
    
    def clear_quizwhiz_form(self):
        self.backup_file_var.set("")
        self.quiz_file_var.set("")
        self.qw_output_var.set("")
        self.merge_mode_var.set("replace")
        self.qw_verbose_var.set(False)
        self.qw_results_text.delete(1.0, tk.END)
        self.qw_progress_var.set("Ready to merge...")
    
    def merge_quizwhiz(self):
        if not self.backup_file_var.get():
            messagebox.showerror("Error", "Please select a QuizWhiz backup file.")
            return
        
        if not self.quiz_file_var.get():
            messagebox.showerror("Error", "Please select a quiz JSON file.")
            return
        
        # Generate output filename if not provided
        output_file = self.qw_output_var.get()
        if not output_file:
            backup_path = Path(self.backup_file_var.get())
            output_file = str(backup_path.parent / f"{backup_path.stem}_UPDATED.json")
        
        append_mode = self.merge_mode_var.get() == "append"
        
        def run_qw_merge():
            self.qw_progress_bar.start()
            self.qw_progress_var.set("Starting QuizWhiz merge...")
            self.qw_results_text.delete(1.0, tk.END)
            
            def progress_callback(message):
                self.root.after(0, lambda: self.qw_progress_var.set(message))
            
            try:
                success, message = merge_quizwhiz_files(
                    self.backup_file_var.get(),
                    self.quiz_file_var.get(),
                    output_file,
                    append_mode=append_mode,
                    verbose=self.qw_verbose_var.get(),
                    progress_callback=progress_callback
                )
                
                self.root.after(0, lambda: self.qw_merge_complete(success, message, output_file))
            except Exception as e:
                self.root.after(0, lambda: self.qw_merge_error(str(e)))
        
        threading.Thread(target=run_qw_merge, daemon=True).start()
    
    def qw_merge_complete(self, success, message, output_file):
        self.qw_progress_bar.stop()
        if not success:
            self.qw_progress_var.set("QuizWhiz merge failed")
            self.qw_results_text.insert(tk.END, f"Error: {message}\n")
            messagebox.showerror("Merge Failed", message)
        else:
            self.qw_progress_var.set("QuizWhiz merge completed successfully")
            self.qw_results_text.insert(tk.END, f"Success: {message}\n")
            self.qw_results_text.insert(tk.END, f"Output file: {output_file}\n")
            messagebox.showinfo("Success", f"QuizWhiz merge completed!\n{message}")
    
    def qw_merge_error(self, error_msg):
        self.qw_progress_bar.stop()
        self.qw_progress_var.set("QuizWhiz merge failed")
        self.qw_results_text.insert(tk.END, f"Error: {error_msg}\n")
        messagebox.showerror("Error", f"QuizWhiz merge failed: {error_msg}")
    
    # Event handlers for transformer tab
    def browse_transform_source(self):
        filename = filedialog.askopenfilename(
            title="Select Source JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.transform_source_var.set(filename)
    
    def browse_transform_backup(self):
        filename = filedialog.askopenfilename(
            title="Select QuizWhiz Backup File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.transform_backup_var.set(filename)
    
    def browse_transform_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Transformed File As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.transform_output_var.set(filename)
    
    def clear_transform_form(self):
        self.transform_source_var.set("")
        self.transform_backup_var.set("")
        self.transform_output_var.set("")
        self.transform_mode_var.set("replace")
        self.transform_verbose_var.set(False)
        self.transform_apply_nlp_var.set(True)
        self.transform_results_text.delete(1.0, tk.END)
        self.transform_progress_var.set("Ready to transform...")
    
    def transform_json(self):
        if not self.transform_source_var.get():
            messagebox.showerror("Error", "Please select a source JSON file.")
            return
        
        # Generate output filename if not provided
        output_file = self.transform_output_var.get()
        if not output_file:
            source_path = Path(self.transform_source_var.get())
            output_file = str(source_path.parent / f"{source_path.stem}_transformed.json")
        
        backup_file = self.transform_backup_var.get() if self.transform_backup_var.get() else None
        append_mode = self.transform_mode_var.get() == "append"
        apply_nlp = self.transform_apply_nlp_var.get()
        
        def run_transform():
            self.transform_progress_bar.start()
            self.transform_progress_var.set("Starting JSON transformation...")
            self.transform_results_text.delete(1.0, tk.END)
            
            def progress_callback(message):
                self.root.after(0, lambda: self.transform_progress_var.set(message))
            
            try:
                success, message = transform_json_structure(
                    self.transform_source_var.get(),
                    output_file,
                    backup_file=backup_file,
                    append_mode=append_mode,
                    apply_nlp=apply_nlp,
                    verbose=self.transform_verbose_var.get(),
                    progress_callback=progress_callback
                )
                
                self.root.after(0, lambda: self.transform_complete(success, message, output_file))
            except Exception as e:
                self.root.after(0, lambda: self.transform_error(str(e)))
        
        threading.Thread(target=run_transform, daemon=True).start()
    
    def transform_complete(self, success, message, output_file):
        self.transform_progress_bar.stop()
        if not success:
            self.transform_progress_var.set("JSON transformation failed")
            self.transform_results_text.insert(tk.END, f"Error: {message}\n")
            messagebox.showerror("Transformation Failed", message)
        else:
            self.transform_progress_var.set("JSON transformation completed successfully")
            self.transform_results_text.insert(tk.END, f"Success: {message}\n")
            self.transform_results_text.insert(tk.END, f"Output file: {output_file}\n")
            messagebox.showinfo("Success", f"JSON transformation completed!\n{message}")
    
    def transform_error(self, error_msg):
        self.transform_progress_bar.stop()
        self.transform_progress_var.set("JSON transformation failed")
        self.transform_results_text.insert(tk.END, f"Error: {error_msg}\n")
        messagebox.showerror("Error", f"JSON transformation failed: {error_msg}")

def main():
    """Main function to run the application"""
    parser = argparse.ArgumentParser(
        description="QuizWhiz JSON Toolkit - All-in-One QuizWhiz JSON Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run GUI mode
  python quiz_toolkit.py
  
  # Run GUI mode in light mode (override system theme)
  python quiz_toolkit.py --light-mode
  
  # Run CLI mode
  python quiz_toolkit.py --cli
  
  # Extract MHTML directly
  python quiz_toolkit.py --extract input.mhtml "My Deck" output.json
  
  # Merge JSON files directly
  python quiz_toolkit.py --merge file1.json file2.json -o merged.json
  
  # Merge with QuizWhiz backup directly
  python quiz_toolkit.py --quizwhiz backup.json quiz.json -o updated.json --append
  
  # Transform JSON with NLP classification
  python quiz_toolkit.py --transform source.json -o transformed.json
  
  # Transform and integrate with QuizWhiz backup
  python quiz_toolkit.py --transform source.json --backup backup.json -o final.json --append
  
  # Transform without NLP classification
  python quiz_toolkit.py --transform source.json --no-nlp -o simple.json
        """
    )
    
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    parser.add_argument('--gui', action='store_true', help='Run in GUI mode (default)')
    parser.add_argument('--light-mode', action='store_true', help='Force GUI to launch in light mode')
    parser.add_argument('--no-banner', action='store_true', help='Disable banner in CLI mode')
    
    # Direct extraction arguments
    parser.add_argument('--extract', nargs=3, metavar=('MHTML', 'DECK', 'OUTPUT'),
                       help='Extract quiz from MHTML file')
    
    # Direct merging arguments
    parser.add_argument('--merge', nargs='+', metavar='FILE',
                       help='Merge multiple JSON files')
    
    # Direct QuizWhiz merging arguments
    parser.add_argument('--quizwhiz', nargs=2, metavar=('BACKUP', 'QUIZ'),
                       help='Merge quiz with QuizWhiz backup')
    
    # Direct JSON transformation arguments
    parser.add_argument('--transform', metavar='SOURCE',
                       help='Transform JSON structure with NLP classification')
    parser.add_argument('--backup', metavar='BACKUP_FILE',
                       help='QuizWhiz backup file for transformation integration')
    parser.add_argument('--no-nlp', action='store_true',
                       help='Skip NLP difficulty classification')
    
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-a', '--append', action='store_true', 
                       help='Append mode for QuizWhiz merge/transform (default: replace)')
    
    args = parser.parse_args()
    
    # Direct operations
    if args.extract:
        if not args.no_banner:
            print_banner()
        mhtml_file, deck_name, output_file = args.extract
        result, message = extract_quiz_from_mhtml(mhtml_file, deck_name, output_file, verbose=args.verbose)
        if result is None:
            print(f"{Colors.FAIL}Error: {message}{Colors.ENDC}")
            sys.exit(1)
        else:
            print(f"{Colors.OKGREEN}Success: {message}{Colors.ENDC}")
        return
    
    if args.merge:
        if not args.no_banner:
            print_banner()
        result_file, message = merge_quiz_files(args.merge, args.output, verbose=args.verbose)
        if result_file is None:
            print(f"{Colors.FAIL}Error: {message}{Colors.ENDC}")
            sys.exit(1)
        else:
            print(f"{Colors.OKGREEN}Success: {message}{Colors.ENDC}")
        return
    
    if args.quizwhiz:
        if not args.no_banner:
            print_banner()
        backup_file, quiz_file = args.quizwhiz
        output_file = args.output
        if not output_file:
            backup_path = Path(backup_file)
            output_file = str(backup_path.parent / f"{backup_path.stem}_UPDATED.json")
        
        success, message = merge_quizwhiz_files(backup_file, quiz_file, output_file, 
                                               append_mode=args.append, verbose=args.verbose)
        if not success:
            print(f"{Colors.FAIL}Error: {message}{Colors.ENDC}")
            sys.exit(1)
        else:
            print(f"{Colors.OKGREEN}Success: {message}{Colors.ENDC}")
        return
    
    if args.transform:
        if not args.no_banner:
            print_banner()
        source_file = args.transform
        output_file = args.output
        if not output_file:
            source_path = Path(source_file)
            output_file = str(source_path.parent / f"{source_path.stem}_transformed.json")
        
        backup_file = args.backup
        append_mode = args.append
        apply_nlp = not args.no_nlp
        
        success, message = transform_json_structure(
            source_file, output_file, backup_file=backup_file,
            append_mode=append_mode, apply_nlp=apply_nlp, 
            verbose=args.verbose
        )
        
        if not success:
            print(f"{Colors.FAIL}Error: {message}{Colors.ENDC}")
            sys.exit(1)
        else:
            print(f"{Colors.OKGREEN}Success: {message}{Colors.ENDC}")
        return
    
    # Interactive modes
    if args.cli:
        cli_workflow()
    else:
        # GUI mode (default)
        try:
            root = tk.Tk()
            app = QuizToolkitGUI(root, force_light_mode=args.light_mode)
            root.mainloop()
        except ImportError:
            print(f"{Colors.WARNING}GUI libraries not available. Running CLI mode instead.{Colors.ENDC}")
            cli_workflow()
        except Exception as e:
            print(f"{Colors.FAIL}Error starting GUI: {e}{Colors.ENDC}")
            print(f"{Colors.WARNING}Falling back to CLI mode.{Colors.ENDC}")
            cli_workflow()

if __name__ == "__main__":
    main()