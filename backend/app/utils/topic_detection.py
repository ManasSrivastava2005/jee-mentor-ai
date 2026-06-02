from app.models.schemas import TopicDetection


TOPIC_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "Mathematics": {
        "Laplace Transform": ["laplace", "inverse laplace", "transform"],
        "Differential Equations": ["differential equation", "dy/dx", "separable", "homogeneous"],
        "Coordinate Geometry": ["circle", "parabola", "ellipse", "hyperbola", "straight line", "locus"],
        "Calculus": ["limit", "derivative", "integral", "continuity", "maxima", "minima"],
        "Probability": ["probability", "binomial", "random variable", "bayes"],
        "Vectors and 3D": ["vector", "dot product", "cross product", "plane", "line in 3d"],
    },
    "Physics": {
        "Electrostatics": ["charge", "electric field", "potential", "capacitor", "gauss"],
        "Thermodynamics": ["heat", "entropy", "adiabatic", "isothermal", "work done", "carnot"],
        "Mechanics": ["projectile", "friction", "newton", "momentum", "kinetic energy"],
        "Optics": ["lens", "mirror", "refraction", "interference", "diffraction"],
        "Modern Physics": ["photoelectric", "bohr", "nucleus", "radioactive", "de broglie"],
    },
    "Chemistry": {
        "Organic Chemistry": ["alkene", "benzene", "reaction mechanism", "reagent", "isomer"],
        "Chemical Thermodynamics": ["enthalpy", "gibbs", "entropy", "free energy"],
        "Electrochemistry": ["nernst", "cell potential", "electrode", "faraday"],
        "Chemical Equilibrium": ["equilibrium", "kp", "kc", "le chatelier", "buffer"],
        "Atomic Structure": ["orbital", "quantum number", "electronic configuration"],
    },
}


def detect_topic(question: str) -> TopicDetection:
    text = question.lower()
    best_subject = "Mathematics"
    best_topic = "General Problem Solving"
    best_hits = 0

    for subject, topics in TOPIC_KEYWORDS.items():
        for topic, keywords in topics.items():
            hits = sum(1 for keyword in keywords if keyword in text)
            if hits > best_hits:
                best_subject = subject
                best_topic = topic
                best_hits = hits

    confidence = min(0.95, 0.48 + best_hits * 0.16) if best_hits else 0.42
    return TopicDetection(subject=best_subject, topic=best_topic, confidence_score=round(confidence, 2))
