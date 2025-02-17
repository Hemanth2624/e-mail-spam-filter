class EmailClassifier:
    def __init__(self):
        # Define classification rules and thresholds
        self.spam_threshold = 0.6
        self.harm_threshold = 0.7

    def classify_email(self, features):
        # Calculate risk scores
        spam_score = self._calculate_spam_score(features)
        harm_score = self._calculate_harm_score(features)
        
        # Determine classification
        if harm_score >= self.harm_threshold:
            return "Harmful", harm_score, self._get_harm_explanation(features)
        elif spam_score >= self.spam_threshold:
            return "Spam", spam_score, self._get_spam_explanation(features)
        else:
            return "Safe", max(1 - spam_score, 1 - harm_score), self._get_safe_explanation(features)

    def _calculate_spam_score(self, features):
        score = 0
        if features['has_urgent']: score += 0.3
        if features['has_money']: score += 0.3
        if features['has_action_required']: score += 0.2
        if features['caps_ratio'] > 0.3: score += 0.2
        return min(score, 1.0)

    def _calculate_harm_score(self, features):
        score = 0
        if features['has_sensitive']: score += 0.4
        if features['has_action_required']: score += 0.2
        if features['has_urgent']: score += 0.2
        if features['has_money']: score += 0.2
        return min(score, 1.0)

    def _get_spam_explanation(self, features):
        reasons = []
        if features['has_urgent']: reasons.append("Contains urgent language")
        if features['has_money']: reasons.append("Contains references to money")
        if features['has_action_required']: reasons.append("Contains call-to-action phrases")
        if features['caps_ratio'] > 0.3: reasons.append("Excessive use of capital letters")
        return reasons if reasons else ["Contains patterns typical of spam messages"]

    def _get_harm_explanation(self, features):
        reasons = []
        if features['has_sensitive']: reasons.append("Requests sensitive information")
        if features['has_action_required']: reasons.append("Contains suspicious call-to-action")
        if features['has_urgent']: reasons.append("Uses urgency to prompt action")
        return reasons if reasons else ["Contains potentially harmful patterns"]

    def _get_safe_explanation(self, features):
        return ["No suspicious patterns detected",
                "Normal content structure",
                "Absence of common spam/harm indicators"]
