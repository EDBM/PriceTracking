import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import desc

from src.services.product_service import ProductService
from .price_chart import PriceChart


class ProductList:
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
        self.price_chart = PriceChart()

    def render(self, products):
        for product in products:
            with st.container():
                st.markdown(f"#### {product.name}")

                col1, col2, col3 = st.columns([1, 3, 1])

                # Display product image
                try:
                    col1.image(product.main_image_url, use_container_width=True)
                except Exception as e:
                    col1.error("Image could not be loaded for this product.")

                # Get price history
                price_history = self.product_service.repository.get_price_history(
                    product.url
                )

                if price_history:
                    # Convert to DataFrame for plotting
                    df = pd.DataFrame(
                        [
                            {"timestamp": ph.timestamp, "price": ph.price}
                            for ph in price_history
                        ]
                    )

                    # Create and display chart
                    fig = self.price_chart.create(df)
                    col2.plotly_chart(fig, use_container_width=True)

                    # Show current price
                    latest_price = price_history[-1].price
                    col3.metric("Current Price", f"{latest_price:.2f} {self.product_service.repository.get(product.url).currency}", delta=f"{latest_price - price_history[-2].price:.2f} {self.product_service.repository.get(product.url).currency}" if len(price_history) > 1 else "N/A", delta_color="inverse")
                else:
                    col2.info("No price history available")

                    #Show if product is on sale and if so, show the price and the full price, if member price is available distinguish between member price and full price and sale price
                    if product.sale_price:
                        col2.success("Product is on sale!")
                        col3.metric("Sale Price", f"{product.sale_price:.2f} {self.product_service.repository.get(product.url).currency}", delta=f"{product.sale_price - product.full_price:.2f} {self.product_service.repository.get(product.url).currency}" if product.full_price else "N/A", delta_color="inverse")
                    else:
                        col2.error("Product is not on sale")
                        #col3.metric("Full Price", f"{product.full_price:.2f} {self.product_service.repository.get(product.url).currency}", delta=f"{product.full_price - product.sale_price:.2f} {self.product_service.repository.get(product.url).currency}" if product.sale_price else "N/A", delta_color="inverse")
                    # Show if product has member price and if so, show the price
                    if product.has_member_price:
                        col2.success("Product has member price!")
                        col3.metric("Member Price", f"{product.member_price:.2f} {self.product_service.repository.get(product.url).currency}", delta=f"{product.member_price - product.full_price:.2f} {self.product_service.repository.get(product.url).currency}" if product.full_price else "N/A", delta_color="inverse")
                    else:
                        col2.error("Product does not have member price")



                # Add visit product button
                col3.link_button("Visit Product", product.url)

                if st.button("Remove from tracking", key=f"remove_{product.url}"):
                    self.product_service.remove_product(product.url)
                    st.success("Product removed from tracking!")
                    st.rerun()
            st.markdown("--------")