import React from "react";

interface ShoppingList {
  id: number;
  order: string;
  isOrdered: boolean;
}

const mockShoppingList: ShoppingList[] = [
  {
    id: 1,
    order: "Oranges",
    isOrdered: true,
  },
  {
    id: 2,
    order: "Milk",
    isOrdered: false,
  },
  {
    id: 3,
    order: "Rice",
    isOrdered: true,
  },
];

const Shopping: React.FC = () => {
  return (
    <div className="dashboard-box shopping-widget">
      <h2>Shopping</h2>
      <div className="shopping-container">
        
        <section className="shopping-list">
          {mockShoppingList.map((orders) => (
            <div
              key={orders.id}
              className={`shopping-item ${orders.isOrdered ? "shopping-ordered" : "shopping-notOrdered"}`}
            >
              <div className="shopping-order">{orders.order}</div>
              <div className="shopping-isOrdered">{orders.isOrdered ? "Ordered, on the way" : "Not ordered"}</div>
            </div>
          ))}
        </section>
      </div>
    </div>
  );
};

export default Shopping;
