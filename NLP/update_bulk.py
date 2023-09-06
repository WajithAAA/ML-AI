@main.route("/<source>/update/bulk", methods=["POST"])
def contacts_update_bulk(source):
    entries = []

    if source not in Config.SOURCE_CONTACT:
        error = logger.error("No such collection in the database")
        return error

    print("File Received")
    print("New Update Request Received")
    request_id = request.form.get("request_id", "")
    file_name = request.form.get("input_file_path", "")

    if request_id == "":
        response = {
            "status": "error",
            "request_id": request_id,
            "info": {
                "message": "REQUEST_ID is required to complete the request",
            }
        }
        return jsonify(response)

    elif not os.path.exists(file_name):
        response = {
            "status": "Error",
            "request_id": request_id,
            "info": {
                "message": f"File not found",
            }
        }
        return jsonify(response)

    elif file_name == "":
        response = {
            "status": "error",
            "request_id": request_id,
            "info": {
                "message": "File not found",
            }
        }
        return jsonify(response)

    else:
        df = pd.read_csv(filepath_or_buffer=file_name)

        try:
            for index, row in df.iterrows():
                party_role_id = str(row["PARTYROLEID"]).strip()
                first_name = str(row["FIRSTNAME"]).strip()
                last_name = str(row["LASTNAME"]).strip()
                mobile_num = str(row["MOBILE_NUMBER"]).strip()
                mobile_num_ext = str(row["MOBILE_NUMBER_EXT"]).strip()
                direct_num = str(row["DIRECT_NUMBER"]).strip()
                direct_num_ext = str(row["DIRECT_NUMBER_EXT"]).strip()
                home_num = str(row["HOME_NUMBER"]).strip()
                home_num_ext = str(row["HOME_NUMBER_EXT"]).strip()
                business_email = str(row["BUSINESS_EMAIL"]).strip()
                personal_email = str(row["PERSONAL_EMAIL"]).strip()
                other_email = str(row["OTHER_EMAIL"]).strip()
                website = str(row["WEBSITE"]).strip()

                query = {'_id': party_role_id}
                update_request = {
                    "_id": party_role_id,
                    "PARTYROLEID": party_role_id,
                    "FIRSTNAME": first_name,
                    "LASTNAME": last_name,
                    "MOBILE_NUMBER": mobile_num,
                    "MOBILE_NUMBER_EXT": mobile_num_ext,
                    "DIRECT_NUMBER": direct_num,
                    "DIRECT_NUMBER_EXT": direct_num_ext,
                    "HOME_NUMBER": home_num,
                    "HOME_NUMBER_EXT": home_num_ext,
                    "BUSINESS_EMAIL": business_email,
                    "PERSONAL_EMAIL": personal_email,
                    "OTHER_EMAIL":other_email,
                    "WEBSITE": website
                }

                entries.append(update_request)

            df_master_o = pd.DataFrame.from_records(entries)
            df_master_o = replace_empty(df_master_o)
            df_master = preprocess_contacts_input(df_master_o, 'MASTER')
            df_master = df_master.replace('nan', '', regex=True)
            df_master = df_master.replace('not available', '', regex=True)

            df_master["_id"] = df_master["_id"].astype(str)
            df_master["PARTYROLEID"] = df_master["PARTYROLEID"].astype(str)

            processed_entries = df_master.to_dict('records')

            update_query = {
            "$set": processed_entries}

            result = mongo.db.master_index_contacts.update_many(query, update_query)

            if result.matched_count > 0:
                response = {
                    "status": "Success",
                    "request_id": request_id,
                    "info": {
                        "message": f"Successfully Updated {len(entries)} Record",
                        "file_name": file_name
                    }
                }
                transaction = {
                    "_id": str(uuid.uuid4()),
                    "REQUEST_ID": request_id,
                    "TRANSACTION_COUNT": len(entries),
                    "API": "Contacts - Update Single Entry",
                    "CREATED_ON": datetime.utcnow().timestamp(),
                }

                mongo.db.master_index_contacts.insert_many(transaction)

                print("Clearing Cache")
                cache.clear()
                print("Cache Cleared")

                _ = reload_master_contacts_to_memory()

                return jsonify(response)

            else:
                response = {
                    "status": "Success",
                    "request_id": request_id,
                    "info": {
                        "message": "Contact not found",

                    }
                }
                return jsonify(response)

        except BulkWriteError as e:
            response = {
                "status": "Success",
                "request_id": request_id,
                "info": {
                    "message": "Duplicate IDs encountered and ignored",
                    "file_name": file_name,
                    "inserted": e.details['nInserted'],
                    "duplicates": [x['op']["_id"] for x in e.details['writeErrors']]
                }
            }
            return jsonify(response)

