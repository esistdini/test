from app import app, db
from models import User, BlogPost, Product, Tag
from werkzeug.security import generate_password_hash
import logging

def seed_database():
    with app.app_context():
        # Check if admin user already exists
        if User.query.filter_by(username='Dinesh').first() is None:
            logging.info("Creating admin user 'Dinesh'")
            # Create admin user
            admin_user = User(
                username='Dinesh',
                email='kogabemanagement@gmail.com',
                password_hash=generate_password_hash('!@#$%^&*')
            )
            db.session.add(admin_user)
            db.session.commit()
            
            # Create a sample blog post
            sample_post = BlogPost(
                title='Welcome to Kogabe Security Blog',
                slug='welcome-to-kogabe-security-blog',
                content='''
                <h2>Welcome to Our Security Blog</h2>
                <p>At Kogabe, we're committed to keeping you informed about the latest developments in cyber security. Our team of experts will be regularly sharing insights, best practices, and tips to help you protect your digital assets.</p>
                
                <h3>What to Expect</h3>
                <p>Our blog will cover a wide range of topics including:</p>
                <ul>
                    <li>Web application security</li>
                    <li>Network security testing</li>
                    <li>Phishing awareness</li>
                    <li>Vulnerability assessments</li>
                    <li>Industry trends and news</li>
                </ul>
                
                <h3>Stay Connected</h3>
                <p>We invite you to bookmark our blog and check back regularly for new content. If you have questions or topics you'd like us to cover, please <a href="/contact">contact us</a>.</p>
                
                <p>Thank you for choosing Kogabe for your security needs!</p>
                ''',
                summary='Learn about our new blog and what to expect from Kogabe\'s security experts',
                published=True,
                author_id=admin_user.id
            )
            db.session.add(sample_post)
            db.session.commit()
            logging.info("Created sample blog post")
            
            # Create tags
            security_tag = Tag.query.filter_by(name='Cyber Security', type='blog').first()
            if not security_tag:
                security_tag = Tag(name='Cyber Security', type='blog')
                db.session.add(security_tag)
            
            product_tag1 = Tag.query.filter_by(name='Network Security', type='product').first()
            if not product_tag1:
                product_tag1 = Tag(name='Network Security', type='product')
                db.session.add(product_tag1)
                
            product_tag2 = Tag.query.filter_by(name='Enterprise', type='product').first()
            if not product_tag2:
                product_tag2 = Tag(name='Enterprise', type='product')
                db.session.add(product_tag2)
                
            db.session.commit()
            
            # Add tag to blog post
            sample_post.tags.append(security_tag)
            db.session.commit()
            logging.info("Added tags to blog post")
            
            # Create a sample product
            sample_product = Product.query.filter_by(title='Network Security Scanner').first()
            if not sample_product:
                sample_product = Product(
                    title='Network Security Scanner',
                    content='''
                    <h2>Comprehensive Network Security Scanner</h2>
                    <p>Our flagship Network Security Scanner provides enterprise-grade protection for your organization's infrastructure. 
                    Designed to identify and analyze vulnerabilities across your network, this scanner helps prevent security breaches before they occur.</p>
                    
                    <h3>Advanced Protection for Modern Threats</h3>
                    <p>In today's rapidly evolving threat landscape, traditional security measures are often insufficient. The Network Security Scanner 
                    employs advanced heuristic detection algorithms and real-time threat intelligence to stay ahead of emerging threats.</p>
                    ''',
                    meta_description='Enterprise-grade network security scanner with real-time monitoring and vulnerability assessment capabilities',
                    key_features='Real-time monitoring and alerts\nIntuitive management dashboard\nSeamless integration with existing systems\nComprehensive reporting and analytics\nAutomated patch verification',
                    compatibility='Windows, Linux, macOS',
                    updates='Automatic security definition updates',
                    support='24/7 Technical Support',
                    license_type='Subscription-based',
                    published=True,
                    author_id=admin_user.id
                )
                db.session.add(sample_product)
                db.session.commit()
                
                # Add tags to product
                sample_product.tags.append(product_tag1)
                sample_product.tags.append(product_tag2)
                db.session.commit()
                logging.info("Created sample product with tags")
            
        else:
            logging.info("Admin user already exists, skipping seed")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    seed_database()
    logging.info("Database seeding complete")