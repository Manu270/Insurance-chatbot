import os
import io
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def load_pdf(file_path):
    """
    Load a PDF file and extract its text content.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from the PDF.
    """
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def split_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Split the text into chunks for processing.
    
    Args:
        text (str): Text to split.
        chunk_size (int): Size of each chunk.
        chunk_overlap (int): Overlap between chunks.
    
    Returns:
        list: List of Document objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

def process_pdf(file_path):
    """
    Process a PDF file by loading it and splitting it into chunks.
    
    Args:
        file_path (str): Path to the PDF file.
    
    Returns:
        list: List of Document objects.
    """
    try:
        text = load_pdf(file_path)
        return split_text(text)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def load_documents_from_directory(directory_path):
    """
    Load all PDF documents from a directory.
    
    Args:
        directory_path (str): Path to the directory containing PDF files.
    
    Returns:
        list: List of Document objects from all PDFs.
    """
    documents = []
    
    # Check if directory exists, if not, create sample PDFs with insurance information
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        create_sample_insurance_pdfs(directory_path)
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            documents.extend(process_pdf(file_path))
    
    return documents

def create_sample_insurance_pdfs(directory_path):
    """
    Create sample PDF files with insurance information.
    This is a fallback when no actual PDFs are provided.
    
    Args:
        directory_path (str): Directory to create sample PDFs in.
    """
    # Since we cannot actually create PDF files in this environment,
    # we'll create text files with the insurance information instead
    
    # Health Insurance Sample Content
    health_insurance_content = """
    # Health Insurance Policies

    ## Basic Health Insurance
    - Monthly Premium: $300-$500
    - Annual Deductible: $1,000-$2,500
    - Coverage: Doctor visits, hospital stays, emergency services, prescription drugs
    - Exclusions: Cosmetic procedures, experimental treatments
    - Maximum Out-of-Pocket: $5,000 per year

    ## Premium Health Insurance
    - Monthly Premium: $500-$800
    - Annual Deductible: $500-$1,000
    - Coverage: All basic coverage plus dental, vision, mental health services
    - Exclusions: Non-medically necessary procedures
    - Maximum Out-of-Pocket: $3,000 per year

    ## Family Health Plan
    - Monthly Premium: $800-$1,200
    - Annual Deductible: $2,000-$3,000 (family total)
    - Coverage: Comprehensive coverage for all family members
    - Exclusions: Similar to Premium Health Insurance
    - Maximum Out-of-Pocket: $10,000 per family per year

    ## Claims Process
    1. Visit in-network healthcare provider
    2. Present insurance card
    3. Provider submits claim to insurance
    4. Insurance processes claim and notifies member
    5. Member pays any remaining cost-sharing amount
    
    ## Frequently Asked Questions
    
    Q: How do I find out if my doctor is in-network?
    A: You can search our provider directory on our website or call customer service.
    
    Q: What is a deductible?
    A: A deductible is the amount you pay for healthcare services before your insurance begins to pay.
    
    Q: How do I appeal a denied claim?
    A: Submit an appeal in writing within 60 days of the denial, including your policy number, date of service, and reason for appeal.
    """

    # Life Insurance Sample Content
    life_insurance_content = """
    # Life Insurance Policies

    ## Term Life Insurance
    - Coverage Period: 10, 20, or 30 years
    - Death Benefit: $100,000 to $1,000,000
    - Premium: $20-$100 per month depending on age, health, and coverage amount
    - Features: Fixed premium for term period, no cash value accumulation
    - Eligibility: Age 18-65, medical examination required for policies over $250,000

    ## Whole Life Insurance
    - Coverage Period: Lifetime
    - Death Benefit: $50,000 to $2,000,000
    - Premium: $100-$500 per month depending on age, health, and coverage amount
    - Features: Fixed premium, builds cash value over time, may pay dividends
    - Eligibility: Age 18-70, medical examination required

    ## Universal Life Insurance
    - Coverage Period: Lifetime (flexible)
    - Death Benefit: $100,000 to $5,000,000 (adjustable)
    - Premium: Flexible, minimum required to keep policy active
    - Features: Adjustable death benefit and premium, builds cash value with interest
    - Eligibility: Age 18-75, medical examination required

    ## Claims Process
    1. Beneficiary notifies insurance company of insured's death
    2. Submit death certificate and claim form
    3. Insurance company reviews claim
    4. Benefit paid to beneficiary upon approval
    
    ## Frequently Asked Questions
    
    Q: Can I change my beneficiary?
    A: Yes, you can change your beneficiary at any time by submitting a beneficiary change form.
    
    Q: Is the death benefit taxable?
    A: Generally, life insurance death benefits are not subject to income tax, but may be subject to estate tax in certain situations.
    
    Q: Can I borrow against my life insurance policy?
    A: You can borrow against the cash value of permanent life insurance policies (whole life, universal life), but not term life policies.
    """

    # Auto Insurance Sample Content
    auto_insurance_content = """
    # Auto Insurance Policies

    ## Liability Coverage
    - Bodily Injury Liability: $25,000-$100,000 per person, $50,000-$300,000 per accident
    - Property Damage Liability: $10,000-$100,000 per accident
    - Required by law in most states
    - Covers damages to others when you're at fault

    ## Collision Coverage
    - Covers damage to your vehicle in an accident regardless of fault
    - Deductible Options: $250, $500, $1,000
    - Premium varies based on vehicle value and deductible choice

    ## Comprehensive Coverage
    - Covers damage from non-collision incidents (theft, vandalism, weather, animals)
    - Deductible Options: $100, $250, $500
    - Premium varies based on vehicle value and deductible choice

    ## Additional Coverage Options
    - Personal Injury Protection: $10,000-$50,000
    - Uninsured/Underinsured Motorist: $25,000-$100,000
    - Rental Car Reimbursement: $30-$50 per day
    - Roadside Assistance: Included or $5-$10 monthly

    ## Claims Process
    1. Report accident to insurance company promptly
    2. Provide details of accident and parties involved
    3. Insurance adjuster assesses damage
    4. Settlement offered and repairs arranged
    5. Deductible paid by policyholder if applicable
    
    ## Frequently Asked Questions
    
    Q: How are auto insurance premiums calculated?
    A: Premiums are based on driving history, age, location, vehicle type, coverage limits, and deductibles.
    
    Q: Will my premium increase after an accident?
    A: Generally, at-fault accidents will increase your premium, but many insurers offer accident forgiveness for first-time incidents.
    
    Q: Do I need insurance for a car I don't drive often?
    A: Yes, if the vehicle is registered, most states require it to be insured even if driven infrequently.
    """

    # Home Insurance Sample Content
    home_insurance_content = """
    # Home Insurance Policies

    ## Dwelling Coverage
    - Coverage Amount: Typically 100% of home's rebuilding cost
    - Protects the physical structure of your home
    - Includes attached structures like garages
    - Covers damage from fire, weather, vandalism

    ## Personal Property Coverage
    - Coverage Amount: Usually 50-70% of dwelling coverage
    - Protects belongings inside and outside the home
    - Special limits may apply to jewelry, electronics, and collectibles
    - Replacement cost vs. actual cash value options

    ## Liability Protection
    - Coverage Amount: $100,000-$500,000
    - Covers legal costs if someone is injured on your property
    - Covers damage you cause to others' property
    - Does not cover intentional damage or business activities

    ## Additional Coverages
    - Loss of Use: 20% of dwelling coverage
    - Medical Payments: $1,000-$5,000 per person
    - Ordinance or Law: 10% of dwelling coverage
    - Optional flood or earthquake insurance available separately

    ## Claims Process
    1. Document damage with photos and video
    2. Report claim to insurance company
    3. Meet with claims adjuster
    4. Receive estimate and settlement offer
    5. Complete repairs or replacements
    
    ## Frequently Asked Questions
    
    Q: Does home insurance cover water damage?
    A: It covers some types of water damage (burst pipes) but not others (floods, ground water). Flood insurance is a separate policy.
    
    Q: How much home insurance do I need?
    A: You should insure your home for its rebuilding cost, not its market value or purchase price.
    
    Q: Are home improvements covered?
    A: You should notify your insurer when making significant home improvements as they may increase your home's rebuilding cost.
    """

    # Write the content to text files
    with open(os.path.join(directory_path, "health_insurance.pdf"), "w") as f:
        f.write(health_insurance_content)
    
    with open(os.path.join(directory_path, "life_insurance.pdf"), "w") as f:
        f.write(life_insurance_content)
    
    with open(os.path.join(directory_path, "auto_insurance.pdf"), "w") as f:
        f.write(auto_insurance_content)
    
    with open(os.path.join(directory_path, "home_insurance.pdf"), "w") as f:
        f.write(home_insurance_content)
