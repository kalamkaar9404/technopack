"""
Crowd-Sourced Anomaly Database
Feature 16: Global anomaly sharing and prevention
"""
import json
import hashlib
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AnomRecord:
    """Anonymized anomaly record"""
    anomaly_id: str
    product_category: str  # water/oil/syrup/carbonated
    viscosity_range: str  # low/medium/high
    temperature_range: str  # cold/room/warm
    issue_type: str  # foam/clog/drift/underfill/overfill
    conditions: Dict  # Anonymized conditions
    solution: str  # What fixed it
    effectiveness: float  # 0-1, how well solution worked
    timestamp: datetime
    upvotes: int  # Community validation

@dataclass
class AnomalySimilarity:
    """Similarity match result"""
    anomaly_id: str
    similarity_score: float  # 0-1
    issue_type: str
    solution: str
    effectiveness: float
    upvotes: int

class AnomalyDatabase:
    """
    Global database of anonymized anomalies and solutions.
    Enables learning from collective experience without sharing sensitive data.
    """
    
    def __init__(self, db_path: str = "./data/anomaly_db.json"):
        """
        Initialize anomaly database.
        
        Args:
            db_path: Path to JSON database file
        """
        self.db_path = Path(db_path)
        self.anomalies = []
        self._load_database()
        
        # Similarity thresholds
        self.similarity_threshold = 0.7  # 70% similar to trigger warning
    
    def _load_database(self):
        """Load anomaly database from file"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    self.anomalies = [
                        AnomRecord(**record) for record in data
                    ]
            except Exception as e:
                print(f"Error loading anomaly database: {e}")
                self.anomalies = []
        else:
            # Create empty database
            self.anomalies = []
            self._save_database()
    
    def _save_database(self):
        """Save anomaly database to file"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.db_path, 'w') as f:
                data = [
                    {**asdict(anom), 'timestamp': anom.timestamp.isoformat()}
                    for anom in self.anomalies
                ]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving anomaly database: {e}")
    
    def report_anomaly(self, product_type: str, viscosity: float,
                      temperature: float, issue_type: str,
                      conditions: Dict, solution: str,
                      effectiveness: float = 1.0) -> str:
        """
        Report a new anomaly (anonymized).
        
        Args:
            product_type: Type of product (water/oil/syrup/etc)
            viscosity: Product viscosity
            temperature: Operating temperature
            issue_type: Type of issue encountered
            conditions: Operating conditions when issue occurred
            solution: What fixed the issue
            effectiveness: How well the solution worked (0-1)
            
        Returns:
            Anomaly ID
        """
        # Anonymize data
        anonymized = self._anonymize_anomaly(
            product_type, viscosity, temperature, 
            issue_type, conditions, solution, effectiveness
        )
        
        # Generate unique ID
        anomaly_id = self._generate_anomaly_id(anonymized)
        
        # Create record
        record = AnomRecord(
            anomaly_id=anomaly_id,
            product_category=anonymized['product_category'],
            viscosity_range=anonymized['viscosity_range'],
            temperature_range=anonymized['temperature_range'],
            issue_type=issue_type,
            conditions=anonymized['conditions'],
            solution=solution,
            effectiveness=effectiveness,
            timestamp=datetime.now(),
            upvotes=0
        )
        
        # Add to database
        self.anomalies.append(record)
        self._save_database()
        
        return anomaly_id
    
    def _anonymize_anomaly(self, product_type: str, viscosity: float,
                          temperature: float, issue_type: str,
                          conditions: Dict, solution: str,
                          effectiveness: float) -> Dict:
        """Anonymize anomaly data to protect privacy"""
        
        # Categorize product
        if 'water' in product_type.lower() or 'juice' in product_type.lower():
            product_category = 'thin_liquid'
        elif 'oil' in product_type.lower():
            product_category = 'medium_liquid'
        elif 'honey' in product_type.lower() or 'syrup' in product_type.lower():
            product_category = 'thick_liquid'
        elif 'carbonated' in product_type.lower() or 'soda' in product_type.lower():
            product_category = 'carbonated'
        else:
            product_category = 'other'
        
        # Categorize viscosity
        if viscosity < 0.01:
            viscosity_range = 'low'
        elif viscosity < 1.0:
            viscosity_range = 'medium'
        else:
            viscosity_range = 'high'
        
        # Categorize temperature
        if temperature < 15:
            temperature_range = 'cold'
        elif temperature < 30:
            temperature_range = 'room'
        else:
            temperature_range = 'warm'
        
        # Anonymize conditions (round to ranges)
        anonymized_conditions = {}
        if 'pressure' in conditions:
            # Round to nearest 10
            anonymized_conditions['pressure_range'] = f"{int(conditions['pressure'] / 10) * 10}-{int(conditions['pressure'] / 10) * 10 + 10} PSI"
        
        if 'valve_timing' in conditions:
            # Round to nearest 0.5
            anonymized_conditions['timing_range'] = f"{round(conditions['valve_timing'] * 2) / 2:.1f}s"
        
        if 'nozzle_diameter' in conditions:
            # Round to nearest 1mm
            anonymized_conditions['nozzle_range'] = f"{round(conditions['nozzle_diameter'])}mm"
        
        return {
            'product_category': product_category,
            'viscosity_range': viscosity_range,
            'temperature_range': temperature_range,
            'conditions': anonymized_conditions
        }
    
    def _generate_anomaly_id(self, anonymized_data: Dict) -> str:
        """Generate unique ID for anomaly"""
        data_str = json.dumps(anonymized_data, sort_keys=True)
        hash_obj = hashlib.md5(data_str.encode())
        return hash_obj.hexdigest()[:12]
    
    def check_similar_anomalies(self, product_type: str, viscosity: float,
                                temperature: float, conditions: Dict,
                                top_k: int = 5) -> List[AnomalySimilarity]:
        """
        Check for similar past anomalies.
        
        Args:
            product_type: Current product type
            viscosity: Current viscosity
            temperature: Current temperature
            conditions: Current operating conditions
            top_k: Number of top matches to return
            
        Returns:
            List of similar anomalies with solutions
        """
        # Anonymize current conditions
        current = self._anonymize_anomaly(
            product_type, viscosity, temperature,
            '', conditions, '', 1.0
        )
        
        # Calculate similarity with all anomalies
        similarities = []
        
        for anomaly in self.anomalies:
            score = self._calculate_similarity(current, anomaly)
            
            if score >= self.similarity_threshold:
                similarities.append(AnomalySimilarity(
                    anomaly_id=anomaly.anomaly_id,
                    similarity_score=score,
                    issue_type=anomaly.issue_type,
                    solution=anomaly.solution,
                    effectiveness=anomaly.effectiveness,
                    upvotes=anomaly.upvotes
                ))
        
        # Sort by similarity score and upvotes
        similarities.sort(
            key=lambda x: (x.similarity_score, x.upvotes, x.effectiveness),
            reverse=True
        )
        
        return similarities[:top_k]
    
    def _calculate_similarity(self, current: Dict, anomaly: AnomRecord) -> float:
        """Calculate similarity score between current conditions and anomaly"""
        score = 0.0
        weights = {
            'product_category': 0.3,
            'viscosity_range': 0.3,
            'temperature_range': 0.2,
            'conditions': 0.2
        }
        
        # Product category match
        if current['product_category'] == anomaly.product_category:
            score += weights['product_category']
        
        # Viscosity range match
        if current['viscosity_range'] == anomaly.viscosity_range:
            score += weights['viscosity_range']
        
        # Temperature range match
        if current['temperature_range'] == anomaly.temperature_range:
            score += weights['temperature_range']
        
        # Conditions similarity
        current_cond = current['conditions']
        anomaly_cond = anomaly.conditions
        
        matching_conditions = sum(
            1 for key in current_cond
            if key in anomaly_cond and current_cond[key] == anomaly_cond[key]
        )
        
        total_conditions = len(set(current_cond.keys()) | set(anomaly_cond.keys()))
        
        if total_conditions > 0:
            condition_similarity = matching_conditions / total_conditions
            score += weights['conditions'] * condition_similarity
        
        return score
    
    def upvote_solution(self, anomaly_id: str) -> bool:
        """
        Upvote a solution that worked.
        
        Args:
            anomaly_id: ID of anomaly to upvote
            
        Returns:
            True if successful
        """
        for anomaly in self.anomalies:
            if anomaly.anomaly_id == anomaly_id:
                anomaly.upvotes += 1
                self._save_database()
                return True
        
        return False
    
    def get_top_solutions(self, issue_type: str, limit: int = 10) -> List[AnomRecord]:
        """
        Get top solutions for a specific issue type.
        
        Args:
            issue_type: Type of issue (foam/clog/drift/etc)
            limit: Maximum number of solutions to return
            
        Returns:
            List of top-rated solutions
        """
        # Filter by issue type
        matching = [
            anom for anom in self.anomalies
            if anom.issue_type == issue_type
        ]
        
        # Sort by effectiveness and upvotes
        matching.sort(
            key=lambda x: (x.effectiveness, x.upvotes),
            reverse=True
        )
        
        return matching[:limit]
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        if len(self.anomalies) == 0:
            return {
                'total_anomalies': 0,
                'issue_types': {},
                'product_categories': {}
            }
        
        # Count by issue type
        issue_counts = {}
        for anom in self.anomalies:
            issue_counts[anom.issue_type] = issue_counts.get(anom.issue_type, 0) + 1
        
        # Count by product category
        product_counts = {}
        for anom in self.anomalies:
            product_counts[anom.product_category] = product_counts.get(anom.product_category, 0) + 1
        
        # Average effectiveness
        avg_effectiveness = sum(a.effectiveness for a in self.anomalies) / len(self.anomalies)
        
        return {
            'total_anomalies': len(self.anomalies),
            'issue_types': issue_counts,
            'product_categories': product_counts,
            'average_effectiveness': avg_effectiveness,
            'total_upvotes': sum(a.upvotes for a in self.anomalies)
        }
    
    def seed_initial_data(self):
        """Seed database with common anomalies"""
        common_anomalies = [
            {
                'product_type': 'carbonated beverage',
                'viscosity': 0.001,
                'temperature': 32.0,
                'issue_type': 'foam_overflow',
                'conditions': {'pressure': 60, 'valve_timing': 1.5},
                'solution': 'Reduce fill speed by 30% and lower temperature to <25°C',
                'effectiveness': 0.95
            },
            {
                'product_type': 'honey',
                'viscosity': 6.0,
                'temperature': 18.0,
                'issue_type': 'clog',
                'conditions': {'nozzle_diameter': 3.0, 'temperature': 18},
                'solution': 'Increase nozzle diameter to 5mm or warm product to 25°C',
                'effectiveness': 0.90
            },
            {
                'product_type': 'oil',
                'viscosity': 0.065,
                'temperature': 25.0,
                'issue_type': 'drift',
                'conditions': {'pressure': 50, 'valve_timing': 2.0},
                'solution': 'Implement temperature compensation - viscosity changes with temp',
                'effectiveness': 0.85
            },
            {
                'product_type': 'water',
                'viscosity': 0.001,
                'temperature': 25.0,
                'issue_type': 'underfill',
                'conditions': {'pressure': 30, 'valve_timing': 1.0},
                'solution': 'Increase pressure to 45 PSI or extend timing to 1.5s',
                'effectiveness': 0.98
            },
            {
                'product_type': 'syrup',
                'viscosity': 2.5,
                'temperature': 35.0,
                'issue_type': 'overfill',
                'conditions': {'pressure': 70, 'valve_timing': 2.5},
                'solution': 'Reduce pressure to 55 PSI - liquid warmed up and flows faster',
                'effectiveness': 0.92
            }
        ]
        
        for anom_data in common_anomalies:
            self.report_anomaly(**anom_data)
        
        print(f"Seeded {len(common_anomalies)} common anomalies")
