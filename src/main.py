import os
import argparse
from input_processor import InputProcessor
from code_analyzer import CodeAnalyzer
from code_improver import CodeImprover
from output_generator import OutputGenerator
from config_manager import ConfigManager
from utils.logger import setup_logger

def main():
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument('input_path', help="Path to codebase (ZIP, folder, or Git URL)")
    parser.add_argument('--output-dir', default='output', help="Output directory for improved code")
    parser.add_argument('--config', default='configs/default_config.json', help="Configuration file")
    args = parser.parse_args()

    logger = setup_logger()
    config_manager = ConfigManager(args.config)
    
    logger.info("Starting code review process...")
    processor = InputProcessor(config_manager)
    analyzer = CodeAnalyzer(config_manager)
    improver = CodeImprover(config_manager)
    generator = OutputGenerator(config_manager)

    try:
        codebase_structure = processor.process_input(args.input_path)
        logger.info("Input processed. Analyzing codebase...")
        issues = analyzer.analyze_codebase(codebase_structure)
        logger.info("Analysis complete. Improving codebase...")
        improved_files, corrected_files = improver.improve_codebase(codebase_structure, issues)
        logger.info("Improvement complete. Generating reports...")
        generator.generate_output(codebase_structure, issues, improved_files + corrected_files, args.output_dir)
        logger.info("Code review completed successfully.")
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == '__main__':
    main()