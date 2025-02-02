
import React, { useState, useEffect, useRef } from "react";
import ReactFlow, { Controls, Background, useReactFlow } from "reactflow";
import "reactflow/dist/style.css";
import MermaidGraph from "./MermaidGraph"
import mermaid from "mermaid";
// Sample JSON data
const jsonData = [
  {
    "authors": "Michel Boyer, Rotem Liss, Tal Mor",
    "coi": "No explicit conflicts of interest section was present in the provided excerpt of the paper.",
    "content": "Composable security against collective attacks of a\nmodiﬁed BB84 QKD protocol with information only in one\nbasis$\nMichel Boyera, Rotem Lissb,∗, Tal Morb\naD´epartement IRO, Universit´e de Montr´eal, Montr´eal (Qu´ebec) H3C 3J7, Canada\nbComputer Science Department, Technion, Haifa 3200003, Israel\nAbstract\nQuantum Cryptography uses the counter-intuitive properties of Quantum Mechanics\nfor performing cryptographic tasks in a secure and reliable way. The Quantum Key\nDistribution (QKD) protocol BB84 has been proven secure against several important\ntypes of attacks: collective attacks and joint attacks. Here we analyze the security of a\nmodiﬁed BB84 protocol, for which information is sent only in the z basis while testing\nis done in both the z and the x bases, against collective attacks. The proof follows\nthe framework of a previous paper [1], but it avoids a classical information-theoretical\nanalysis and proves a fully composable security. We show that this modiﬁed BB84\nprotocol is as secure against collective attacks as the original BB84 protocol, and that\nit requires more bits for testing.\nKeywords: Collective Attacks, Quantum Key Distribution, Cryptography, Error Rate,\nTest Bits, Information Bits.\n1. Introduction\nCryptography is the science of protecting the security and correctness of data against\nadversaries. One of the most important cryptographic problems is the problem of en-\ncryption – namely, of transmitting a secret message from a sender to a receiver. Two\nmain encryption methods are used today:\n1. In symmetric-key cryptography, the same secret key is used for both the sender\nand the receiver: the sender uses the secret key for encrypting his or her message,\nand the receiver uses the same secret key for decrypting the message. Examples\nof symmetric-key ciphers include the Advanced Encryption Standard (AES) [3],\nthe older Data Encryption Standard (DES), and one-time pad (“Vernam cipher”).\n$A preliminary version of this paper appeared in Proceedings of the 2nd International Conference on\nComplexity, Future Information Systems and Risk – COMPLEXIS, 24-26 April, 2017, Porto, Portugal [2].\n∗Corresponding author\nEmail addresses: boyer@iro.umontreal.ca (Michel Boyer), rotemliss@cs.technion.ac.il\n(Rotem Liss), talmo@cs.technion.ac.il (Tal Mor)\nPreprint submitted to Elsevier\nNovember 20, 2019\narXiv:1711.09716v2  [quant-ph]  19 Nov 2019\n2. In public-key cryptography [4], a public key (known to everyone) and a secret\nkey (known only to the receiver) are used: the sender uses the public key for\nencrypting his or her message, and the receiver uses the secret key for decrypting\nthe message. Examples of public-key ciphers include RSA [5] and elliptic curve\ncryptography.\nOne of the main problems with current public-key cryptography is that its security is\nusually not formally proved. Moreover, its security relies on the computational hard-\nness of speciﬁc computational problems, such as integer factorization and discrete log-\narithm (that can both be efﬁciently solved on a quantum computer, by using Shor’s fac-\ntorization algorithm [6]; therefore, if a scalable quantum computer is successfully built\nin the future, the security of many public-key ciphers, including RSA and elliptic curve\ncryptography, will be broken). Symmetric-key cryptography requires a secret key to\nbe shared in advance between the sender and the receiver (in other words, if the sender\nand the receiver want to share a secret message, they must share a secret key before-\nhand). Moreover, no security proofs for many current symmetric-key ciphers, such as\nAES and DES, are known (even if one is allowed to rely on the computational hardness\nof problems), and unconditional security proofs against computationally-unlimited ad-\nversaries are impossible unless the secret key is used only once and is at least as long\nas the secret message [7].\nThe one-time pad (symmetric-key) cipher, that, given a message M and a secret\nkey K of the same length, deﬁnes the encrypted message C to",
    "future_research": [
      "Extending the security proof to handle joint/general attacks",
      "Analyzing the protocol's security with imperfect devices",
      "Optimizing the number of test bits required while maintaining security",
      "Investigating practical implementations of the modified protocol"
    ],
    "method_issues": "• The proof assumes collective attacks only and does not address all possible quantum attacks\n• The security analysis assumes perfect quantum devices and does not account for implementation imperfections\n• The protocol requires more test bits compared to standard BB84, which impacts efficiency",
    "name": "Composable security against collective attacks of a modified BB84 QKD protocol with information only in one basis",
    "num_out": 0,
    "out_references": [],
    "publication_date": "2019-11-19",
    "summary": "This paper analyzes the security of a modified BB84 quantum key distribution protocol where information is only sent in the z basis while testing is done in both z and x bases, proving its security against collective attacks. The authors demonstrate that this modified protocol is as secure as the original BB84 protocol but requires more testing bits.",
    "url": "http://arxiv.org/abs/1711.09716v2"
  },
  {
    "authors": "Shi-Hai Sun, Feihu Xu, Mu-Sheng Jiang, Xiang-Chun Ma, Hoi-Kwong Lo, Lin-Mei Liang",
    "coi": "The paper does not appear to contain an explicit conflicts of interest section.",
    "content": "arXiv:1508.05258v1  [quant-ph]  21 Aug 2015\nEﬀect of source tampering in the security of quantum cryptography\nShi-Hai Sun1,∗Feihu Xu2,4,† Mu-Sheng Jiang1, Xiang-Chun Ma1, Hoi-Kwong Lo2,‡ and Lin-Mei Liang1,3§\n1 College of Science, National University of Defense Technology, Changsha 410073, China\n2 Center for Quantum Information and Quantum Control,\nDepartment of Electrical and Computer Enginnering and Department of Physics,\nUniversity of Toronto, Toronto, Ontario, M5S 3G4, Canada\n3State Key Laboratory of High Performance Computing,\nNational University of Defense Technology, Changsha 410073, China\n4 Research Laboratory of Electronics, Massachusetts Institute of Technology,\n77 Massachusetts Avenue, Cambridge, Massachusetts 02139, USA\n(Dated: July 4, 2018)\nThe security of source has become an increasingly important issue in quantum cryptogra-\nphy. Based on the framework of measurement-device-independent quantum-key-distribution (MDI-\nQKD), the source becomes the only region exploitable by a potential eavesdropper (Eve). Phase\nrandomization is a cornerstone assumption in most discrete-variable (DV-) quantum communication\nprotocols (e.g., QKD, quantum coin tossing, weak coherent state blind quantum computing, and so\non), and the violation of such an assumption is thus fatal to the security of those protocols. In this\npaper, we show a simple quantum hacking strategy, with commercial and homemade pulsed lasers,\nby Eve that allows her to actively tamper with the source and violate such an assumption, without\nleaving a trace afterwards. Furthermore, our attack may also be valid for continuous-variable (CV-)\nQKD, which is another main class of QKD protocol, since, excepting the phase random assumption,\nother parameters (e.g., intensity) could also be changed, which directly determine the security of\nCV-QKD.\nI.\nINTRODUCTION\nQuantum key distribution (QKD) [1] allows two re-\nmote parties to share an unconditional secret key, which\nhas been proven in theory [2–4] and demonstrated in ex-\nperiment [5]. However, the imperfections of practical de-\nvices will compromise the security of QKD systems [6–\n14]. So far, three main approaches have been proposed\nto bridge the gap between theory and practice. The ﬁrst\none is to close speciﬁc loopholes of devices with security\npatches [15], but it could not close potential and unno-\nticed loopholes. The second one is device-independent\n(DI-) QKD [16–18].\nBy testing Bells inequality in a\nloophole-free setting, security could be obtained without\ndetailed information about the implementation devices.\nBut DI-QKD is impractical because an almost perfect\nsingle photon detector (SPD) is required, and even so the\nsecret key rate is limited [19, 20]. The third approach is\nto remove as many device loopholes and assumptions as\npossible by either modifying the QKD protocol or reﬁning\nthe security proof. One of the best results with this ap-\nproach is measurement-device-independent (MDI-) QKD\n[21], which can remove all detector loopholes. Since the\ndetection system is widely regarded as the Achilles’ heel\nof QKD [6, 8, 9, 13], MDI-QKD is of great importance.\nIndeed, recently, MDI-QKD has been demonstrated both\nin the laboratory and in the ﬁeld [22].\n∗shsun@nudt.edu.cn\n†tigerfeihuxu@gmail.com\n‡hklo@ece.utoronto.ca\n§nmliang@nudt.edu.cn\nBased on the framework of MDI-QKD, the source be-\ncomes the ﬁnal battleﬁeld for the legitimate parties and\nEve. And the major ﬂaw of the source is that a semicon-\nductor laser diode (S-LD), which generates a weak co-\nherent state, is normally used as a single photon source\nin most commercial and research QKD systems [5, 22].\nThe security of MDI-QKD as well as BB84 based on S-\nLD has been proven with decoy state [23]. Hence, it has\nbeen convinced that if the source can be well character-\nized (for example the source ﬂaws could be taken care of\nwith the loss-tolerant QKD protocol [24]), perfect secu-\nrity can still be obtained.\nGenerally speaking, there are two main classes of QKD\nprotocols",
    "future_research": [
      "Development of countermeasures against source tampering attacks",
      "Investigation of impact on other quantum protocols beyond QKD",
      "Analysis of attack effectiveness on different laser source types",
      "Further study of implications for continuous-variable QKD systems",
      "Development of methods to verify source integrity in deployed systems"
    ],
    "method_issues": "- Assumes specific types of laser sources (semiconductor laser diodes)\n- Focus mainly on discrete-variable QKD systems with less analysis of continuous-variable systems\n- Limited experimental validation with only commercial and homemade pulsed lasers\n- Does not fully explore countermeasures against the proposed attack",
    "name": "Effect of source tampering in the security of quantum cryptography",
    "num_out": 0,
    "out_references": [],
    "publication_date": "2015-08-21",
    "summary": "The paper demonstrates a quantum hacking strategy that exploits vulnerabilities in the source components of quantum cryptography systems, specifically targeting the phase randomization assumption critical to many quantum protocols. The authors show how an eavesdropper could actively tamper with commercial and homemade pulsed lasers used as sources without detection, potentially compromising both discrete-variable and continuous-variable QKD systems.",
    "url": "http://arxiv.org/abs/1508.05258v1"
  },
  {
    "authors": "Kfir Sulimany, Guy Pelc, Rom Dudkiewicz, Simcha Korenblit, Hagai S. Eisenberg, Yaron Bromberg, Michael Ben-Or",
    "coi": "No explicit conflicts of interest section was present in the provided excerpt.",
    "content": "High-dimensional coherent one-way quantum key distribution\nKfir Sulimany1, Guy Pelc1, Rom Dudkiewicz2, Simcha Korenblit1, Hagai S. Eisenberg1, Yaron\nBromberg1 *, and Michael Ben-Or2 *\n1Racah Institute of Physics, The Hebrew University of Jerusalem, Jerusalem 91904, Israel\n2School of Computer Science & Engineering, The Hebrew University of Jerusalem, Jerusalem,\n91904 Israel\n*Corresponding authors: yaron.bromberg@mail.huji.ac.il, benor@cs.huji.ac.il\nAbstract\nHigh-dimensional quantum key distribution (QKD) offers secure communication, with secure key rates that\nsurpass those achievable by QKD protocols utilizing two-dimensional encoding. However, existing high-dimensional\nQKD protocols require additional experimental resources, such as multiport interferometers and multiple detectors,\nthus raising the cost of practical high-dimensional systems and limiting their use. Here, we present and analyze\na novel protocol for arbitrary-dimensional QKD, that requires only the hardware of a standard two-dimensional\nsystem. We provide security proofs against individual attacks and coherent attacks, setting an upper and lower\nbound on the secure key rates. Then, we test the new high-dimensional protocol in a standard two-dimensional\nQKD system over a 40 km fiber link.\nThe new protocol yields a two-fold enhancement of the secure key\nrate compared to the standard two-dimensional coherent one-way protocol, without introducing any hardware\nmodifications to the system. This work, therefore, holds great potential to enhance the performance of already\ndeployed time-bin QKD systems through a software update alone. Furthermore, its applications extend across\ndifferent encoding schemes of QKD qudits.\n1\nIntroduction\nQuantum key distribution (QKD) is an advanced tech-\nnology that provides ultimate secure communication by\nexploiting quantum states of light as information carri-\ners over communication channels [1–5]. In the early QKD\nprotocols, each bit of the key was encoded using a quan-\ntum state belonging to a two-dimensional Hilbert space\n[6, 7]. High-dimensional QKD protocols were introduced\nmore recently, based on preparing a set of states belong-\ning to a high-dimensional Hilbert space, called qudits [8–\n13]. The higher information capacity of qudits allows a\nhigher secure key rate and improves the robustness to\nnoise, leading to higher threshold values of the quantum\nbit error rate (QBER) [14, 15].\nTime-bin encoding of weak coherent laser pulses is\nthe most popular technique for implementing QKD over\nsingle-mode fibers [16–19]. Recent proposals and demon-\nstrations of high-dimensional temporal encoding showed\na significant key rate improvement [20–28]. In particular,\na record-breaking key rate of 26.2 Mbit/s was achieved\nwith a four-dimensional time-bin protocol that is robust\nagainst the most general (coherent) attacks [20].\nFur-\nthermore, high-dimensional time-bin encoding was suc-\ncessfully demonstrated in entanglement-based QKD sys-\ntems over free-space [29], and fiber links [30–32].\nImplementation of high-dimensional QKD protocols in\ncommercial systems is still held back since present high-\ndimensional schemes require significantly more complex\nexperimental resources, relative to the cost-effective two-\ndimensional systems [33]. The large experimental over-\nhead results from the fact that high-dimensional encod-\ning not only increases the channel capacity but also in-\ncreases the amount of information that Eve can extract.\nMost QKD protocols limit the amount of information ac-\ncessible to Eve by projecting the quantum states at the\nreceiver’s end on unbiased bases. While the projection\nin two-dimensional schemes is usually implemented with\na single interferometer followed by a single photon de-\ntector (SPD), to fully exploit the potential capacity of\nd-dimensional schemes, O(d) imbalanced interferometers\nand O(d) SPDs [20–22] are required. Thus, to date, all\nhigh-dimensional QKD systems implementations require\ncomplex and expensive systems tha",
    "future_research": [
      "Testing the protocol over longer distances and different types of fiber links",
      "Exploring applications across different encoding schemes of QKD qudits",
      "Investigating potential vulnerabilities to other types of quantum attacks",
      "Optimizing the protocol for different dimensional spaces",
      "Implementation in commercial QKD systems"
    ],
    "method_issues": "• The security proofs are limited to individual attacks and coherent attacks, potentially leaving other attack vectors unexplored\n• The experimental demonstration was conducted only on a single distance (40km), which might not represent performance across all possible deployment scenarios\n• The protocol assumes perfect timing synchronization between sender and receiver",
    "name": "High-dimensional coherent one-way quantum key distribution",
    "num_out": 0,
    "out_references": [],
    "publication_date": "2023-07-11",
    "summary": "This paper presents a new protocol for high-dimensional quantum key distribution (QKD) that achieves higher secure key rates while using only standard two-dimensional system hardware. The protocol was tested over a 40km fiber link and demonstrated a two-fold enhancement in secure key rate compared to traditional two-dimensional protocols, suggesting potential improvements to existing QKD systems through software updates alone.",
    "url": "http://arxiv.org/abs/2105.04733v5"
  },
  {
    name: "Deep Learning for NLP",
    url: "https://example.com/deep-nlp",
    authors: "John Doe, Jane Smith",
    content: "This paper explores the application of deep learning techniques in natural language processing.",
    publication_date: "2023-06-15",
    out_references: ["Attention Mechanisms", "Language Models"],
    num_out: 2,
    summary: "A comprehensive study on deep learning methods for NLP tasks.",
    method_issues: "Limited dataset diversity.",
    coi: "No conflicts of interest.",
    future_research: "Explore transformer-based models for NLP."
  },
  {
    name: "Attention Mechanisms",
    url: "https://example.com/attention",
    authors: "Alice Brown",
    content: "This paper introduces attention mechanisms and their role in neural networks.",
    publication_date: "2021-05-10",
    out_references: ["Sequence Modelling"],
    num_out: 1,
    summary: "An in-depth analysis of attention mechanisms in deep learning.",
    method_issues: "High computational cost.",
    coi: "No conflicts of interest.",
    future_research: "Optimize attention mechanisms for efficiency."
  },
  {
    name: "Language Models",
    url: "https://example.com/language-models",
    authors: "David Green",
    content: "This paper discusses the evolution of language models in NLP.",
    publication_date: "2022-11-20",
    out_references: ["Transformer Networks"],
    num_out: 1,
    summary: "A review of language models from RNNs to transformers.",
    method_issues: "Lack of interpretability.",
    coi: "No conflicts of interest.",
    future_research: "Improve interpretability of language models."
  },
  {
    name: "Transformer Networks",
    url: "https://example.com/transformers",
    authors: "Emily White",
    content: "This paper presents the transformer architecture and its applications.",
    publication_date: "2019-12-01",
    out_references: ["Neural Machine Translation"],
    num_out: 1,
    summary: "A detailed explanation of transformer networks.",
    method_issues: "Requires large datasets.",
    coi: "No conflicts of interest.",
    future_research: "Apply transformers to low-resource languages."
  },
  {
    name: "Neural Machine Translation",
    url: "https://example.com/nmt",
    authors: "Sophia Johnson, Mark Lee",
    content: "This paper focuses on neural machine translation using transformers.",
    publication_date: "2018-08-30",
    out_references: [],
    num_out: 0,
    summary: "An exploration of NMT systems and their performance.",
    method_issues: "Difficulty with rare languages.",
    coi: "No conflicts of interest.",
    future_research: "Improve translation for low-resource languages."
  },
  {
    name: "Graph Neural Networks",
    url: "https://example.com/gnn",
    authors: "Chris Brown",
    content: "This paper introduces graph neural networks and their applications.",
    publication_date: "2020-04-22",
    out_references: ["Deep Graph Learning"],
    num_out: 1,
    summary: "A comprehensive overview of GNNs and their use cases.",
    method_issues: "Scalability issues.",
    coi: "No conflicts of interest.",
    future_research: "Develop scalable GNN architectures."
  },
  {
    name: "Deep Graph Learning",
    url: "https://example.com/deep-graph",
    authors: "Anna Williams",
    content: "This paper explores deep learning techniques for graph-structured data.",
    publication_date: "2021-09-14",
    out_references: [],
    num_out: 0,
    summary: "A study on deep learning methods for graph data.",
    method_issues: "Limited generalization.",
    coi: "No conflicts of interest.",
    future_research: "Improve generalization of graph models."
  },
  {
    name: "Bayesian Learning Methods",
    url: "https://example.com/bayesian",
    authors: "Robert Wilson",
    content: "This paper discusses Bayesian methods for machine learning.",
    publication_date: "2017-07-19",
    out_references: ["Probabilistic Models"],
    num_out: 1,
    summary: "An introduction to Bayesian learning and its advantages.",
    method_issues: "Computationally intensive.",
    coi: "No conflicts of interest.",
    future_research: "Optimize Bayesian methods for large datasets."
  },
  {
    name: "Probabilistic Models",
    url: "https://example.com/probabilistic",
    authors: "Laura Martinez",
    content: "This paper explores probabilistic models in machine learning.",
    publication_date: "2016-11-05",
    out_references: [],
    num_out: 0,
    summary: "A review of probabilistic models and their applications.",
    method_issues: "Difficulty with high-dimensional data.",
    coi: "No conflicts of interest.",
    future_research: "Extend probabilistic models to high-dimensional spaces."
  },
  {
    name: "Reinforcement Learning",
    url: "https://example.com/rl",
    authors: "Tom Harris",
    content: "This paper discusses reinforcement learning algorithms and their applications.",
    publication_date: "2019-03-08",
    out_references: ["Markov Decision Processes"],
    num_out: 1,
    summary: "An overview of reinforcement learning techniques.",
    method_issues: "Sample inefficiency.",
    coi: "No conflicts of interest.",
    future_research: "Improve sample efficiency in RL."
  },
  {
    name: "Markov Decision Processes",
    url: "https://example.com/mdp",
    authors: "Rachel Adams",
    content: "This paper introduces Markov decision processes and their role in RL.",
    publication_date: "2015-02-14",
    out_references: [],
    num_out: 0,
    summary: "A detailed explanation of MDPs and their applications.",
    method_issues: "Curse of dimensionality.",
    coi: "No conflicts of interest.",
    future_research: "Address dimensionality issues in MDPs."
  },
  {
    name: "Computer Vision with CNNs",
    url: "https://example.com/cnn-vision",
    authors: "James Carter",
    content: "This paper explores convolutional neural networks for computer vision tasks.",
    publication_date: "2021-10-25",
    out_references: ["Image Recognition"],
    num_out: 1,
    summary: "A study on CNNs and their use in computer vision.",
    method_issues: "Overfitting on small datasets.",
    coi: "No conflicts of interest.",
    future_research: "Develop techniques to reduce overfitting."
  },
  {
    name: "Image Recognition",
    url: "https://example.com/image-recognition",
    authors: "Maria Gonzalez",
    content: "This paper focuses on image recognition using deep learning.",
    publication_date: "2020-06-17",
    out_references: [],
    num_out: 0,
    summary: "An exploration of image recognition systems.",
    method_issues: "Sensitivity to adversarial attacks.",
    coi: "No conflicts of interest.",
    future_research: "Improve robustness against adversarial attacks."
  },
  {
    name: "Ethics in AI",
    url: "https://example.com/ai-ethics",
    authors: "Olivia Thompson",
    content: "This paper discusses ethical considerations in AI development.",
    publication_date: "2022-01-09",
    out_references: ["Fairness in Machine Learning"],
    num_out: 1,
    summary: "A review of ethical issues in AI systems.",
    method_issues: "Lack of standardized guidelines.",
    coi: "No conflicts of interest.",
    future_research: "Develop ethical frameworks for AI."
  },
  {
    name: "Fairness in Machine Learning",
    url: "https://example.com/fairness-ml",
    authors: "Daniel Wright",
    content: "This paper explores fairness and bias in machine learning models.",
    publication_date: "2019-12-29",
    out_references: [],
    num_out: 0,
    summary: "A study on fairness metrics and bias mitigation techniques.",
    method_issues: "Trade-offs between fairness and accuracy.",
    coi: "No conflicts of interest.",
    future_research: "Balance fairness and accuracy in ML models."
  },
  {
    name: "Generative Adversarial Networks",
    url: "https://example.com/gan",
    authors: "Ethan Moore",
    content: "This paper introduces GANs and their applications in generative modeling.",
    publication_date: "2020-07-12",
    out_references: ["Image Synthesis"],
    num_out: 1,
    summary: "An overview of GANs and their use cases.",
    method_issues: "Training instability.",
    coi: "No conflicts of interest.",
    future_research: "Improve training stability in GANs."
  },
  {
    name: "Image Synthesis",
    url: "https://example.com/image-synthesis",
    authors: "Sophie Clark",
    content: "This paper focuses on image synthesis using GANs.",
    publication_date: "2021-03-18",
    out_references: [],
    num_out: 0,
    summary: "A study on image synthesis techniques.",
    method_issues: "Mode collapse in GANs.",
    coi: "No conflicts of interest.",
    future_research: "Address mode collapse in GANs."
  },
  {
    name: "Self-Supervised Learning",
    url: "https://example.com/self-supervised",
    authors: "Liam Taylor",
    content: "This paper explores self-supervised learning methods.",
    publication_date: "2022-08-22",
    out_references: ["Contrastive Learning"],
    num_out: 1,
    summary: "A review of self-supervised learning techniques.",
    method_issues: "Requires large amounts of unlabeled data.",
    coi: "No conflicts of interest.",
    future_research: "Optimize self-supervised learning for small datasets."
  },
  {
    name: "Contrastive Learning",
    url: "https://example.com/contrastive",
    authors: "Emma Wilson",
    content: "This paper discusses contrastive learning and its applications.",
    publication_date: "2023-02-14",
    out_references: [],
    num_out: 0,
    summary: "An exploration of contrastive learning methods.",
    method_issues: "Sensitive to negative sample selection.",
    coi: "No conflicts of interest.",
    future_research: "Improve negative sampling strategies."
  },
  {
    name: "Federated Learning",
    url: "https://example.com/federated",
    authors: "Noah Anderson",
    content: "This paper introduces federated learning and its use in distributed systems.",
    publication_date: "2021-11-30",
    out_references: ["Privacy-Preserving ML"],
    num_out: 1,
    summary: "A study on federated learning and its challenges.",
    method_issues: "Communication overhead.",
    coi: "No conflicts of interest.",
    future_research: "Reduce communication costs in federated learning."
  }
];


const processInputData = (data) => {
  // Create a map to store in-references for each node
  const inReferencesMap = new Map();

  // First pass: Populate in-references
  data.forEach((node) => {
    node.out_references.forEach((ref) => {
      if (!inReferencesMap.has(ref)) {
        inReferencesMap.set(ref, []);
      }
      inReferencesMap.get(ref).push(node.name);
    });
  });

  // Second pass: Transform data into the required format
  const transformedData = data.map((node) => ({
    name: node.name,
    url: node.url,
    authors: node.authors, // String 
    publication_date: node.publication_date,
    out_references: node.out_references,
    num_out: node.num_out,
    in_references: inReferencesMap.get(node.name) || [], // Add in-references
    num_in: inReferencesMap.get(node.name)?.length || 0, // Add num_in
  }));

  return transformedData;
};


// Convert JSON to React Flow nodes & edges
const generateGraph = (data) => {
  const sortedData = data.sort((a, b) => b.num_out - a.num_out);
  const totalNodes = sortedData.length;
  const radiusStep = 100 + 5 * totalNodes;
  const nodes = sortedData.map((node, index) => {
    const angle = (index / totalNodes) * 2 * Math.PI;
    const radius = radiusStep * Math.min(index, 2);
    const x = 300 + radius * Math.cos(angle);
    const y = 200 + radius * Math.sin(angle);

    return {
      id: node.name,
      data: { label: node.name },
      position: { x, y }, // Ensure position is defined
    };
  });

  const edges = data.flatMap((node) =>
    node.out_references.map((ref) => ({
      id: `${node.name}-${ref}`,
      source: node.name,
      target: ref,
      animated: true,
      markerEnd: { type: "arrowclosed" }, // Add arrowhead to the edge
    }))
  );

  return { nodes, edges };
};// Calculate node influence based on incoming references
const calculateNodeInfluence = (data) => {
  const maxInReferences = Math.max(...data.map((node) => node.num_in));
  return data.map((node) => ({
    ...node,
    influence: node.num_in / maxInReferences, // Normalize influence to [0, 1]
  }));
};

// Generate CSS gradient based on node positions and influence
const generateBackgroundGradient = (nodes) => {
  let gradient = "radial-gradient(circle, ";

  nodes.forEach((node) => {
    if (node.position && node.position.x !== undefined && node.position.y !== undefined) {
      const { x, y } = node.position;
      const darkness = 100 - Math.floor(node.influence * 50); // Darker for higher influence
      gradient += `rgba(0, 0, 0, ${node.influence * 0.3}) ${x}px ${y}px, `;
    } else {
      console.error("Node missing position:", node);
    }
  });

  gradient = gradient.slice(0, -2) + ")"; // Remove trailing comma and close gradient

  console.log("Final Gradient:", gradient); // Log the final gradient
  return gradient;
};

const App = () => {
  const [graph, setGraph] = useState({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState(null);
  const [backgroundGradient, setBackgroundGradient] = useState("");

  useEffect(() => {
    const processedData = processInputData(jsonData);
    const { nodes, edges } = generateGraph(processedData);
    setGraph({ nodes, edges });

    // Calculate node influence and generate background gradient
    const nodesWithInfluence = calculateNodeInfluence(jsonData);
    const gradient = generateBackgroundGradient(nodesWithInfluence);
    console.log("Generated Gradient:", gradient); // Log the gradient
    setBackgroundGradient(gradient);
  }, []);

  // Handle node clicks
  const handleNodeClick = (event, node) => {
    const nodeData = jsonData.find((item) => item.name === node.id);
    setSelectedNode(nodeData); // Update state with the clicked node's data
  };


  const handleReferenceClick = (referenceName) => {
    const referencedNode = jsonData.find((item) => item.name === referenceName);
    if (referencedNode) {
      setSelectedNode(referencedNode); // Update state with the referenced node's data
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", flexDirection: "row" }}>
      {/* React Flow container */}
      <div
        style={{
          flex: 1,
          position: "relative",
          background: backgroundGradient || "white", // Fallback to white if gradient is empty
        }}
      >
        <h1 style={{ textAlign: "center" }}>Interactive Graph</h1>
        <ReactFlow
          nodes={graph.nodes}
          edges={graph.edges}
          onNodeClick={handleNodeClick} // Attach click handler
        >
          <Controls position="top-left" /> {/* Add controls */}
          <Background /> {/* Add a background */}
        </ReactFlow>
      </div>      {/* Sidebar to display the selected node's data */}
      {selectedNode && (
        <div
          style={{
            width: "30%",
            backgroundColor: "#f4f4f4",
            padding: "20px",
            position: "absolute",
            right: 0,
            top: 0,
            height: "100%",
            overflowY: "auto",
            boxShadow: "-2px 0 5px rgba(0, 0, 0, 0.1)",
          }}
        >
          <h2>Node Details</h2>
          <div>
            <h3>Name: {selectedNode.name}</h3>
            <p><strong>Authors:</strong> {selectedNode.authors}</p>
            <p><strong>Publication Date:</strong> {selectedNode.publication_date}</p>
            <p><strong>URL:</strong> <a href={selectedNode.url} target="_blank" rel="noopener noreferrer">{selectedNode.url}</a></p>



            {/* Out References */}
            <p>
              <strong>References:</strong>
              {selectedNode.num_out > 0 ? (
                selectedNode.out_references.map((ref) => (
                  <button
                    key={ref}
                    onClick={() => handleReferenceClick(ref)}
                    style={{
                      margin: "2px",
                      padding: "4px 8px",
                      background: "#007bff",
                      border: "none",
                      color: "white",
                      cursor: "pointer",
                      borderRadius: "4px",
                    }}
                  >
                    {ref}
                  </button>
                ))
              ) : (
                " None"
              )}
            </p>

            {/* In References */}
            <p>
              <strong>Referenced by:</strong>
              {selectedNode.num_in > 0 ? (
                selectedNode.in_references.map((ref) => (
                  <button
                    key={ref}
                    onClick={() => handleReferenceClick(ref)}
                    style={{
                      margin: "2px",
                      padding: "4px 8px",
                      background: "#28a745",
                      border: "none",
                      color: "white",
                      cursor: "pointer",
                      borderRadius: "4px",
                    }}
                  >
                    {ref}
                  </button>
                ))
              ) : (
                " None"
              )}
            </p>
          </div>
          <button
            onClick={() => setSelectedNode(null)}
            style={{
              marginTop: "20px",
              padding: "10px",
              background: "yellow",
              border: "none",
              color: "blue",
              cursor: "pointer",
              borderRadius: "5px",
            }}
          >
            Close
          </button>
        </div>
      )}
    </div>
  );
};

export default App;
